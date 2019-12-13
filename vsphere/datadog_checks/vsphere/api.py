# (C) Datadog, Inc. 2019
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import ssl
import threading

from pyVim import connect
from pyVmomi import vim, vmodl  # pylint: disable=E0611

from datadog_checks.base import is_affirmative, ensure_unicode
from datadog_checks.vsphere.utils import smart_retry


ALL_RESOURCES = [vim.VirtualMachine, vim.HostSystem, vim.Datacenter, vim.Datastore, vim.ClusterComputeResource, vim.ComputeResource, vim.Folder]
BATCH_COLLETOR_SIZE = 500


class MetricCollector(object):
    """This class is used for collecting metrics from multiple threads.
    """

    def __init__(self, config_instance):
        self._apis = {}
        self.instance = config_instance

    def query_metrics(self, query_specs):
        thread_id = threading.get_ident()
        if thread_id not in self._apis:
            self._apis[thread_id] = VSphereAPI(self.instance)

        return self._apis[thread_id].query_metrics(query_specs)


class VSphereAPI(object):
    """Abstraction class over vSphere SOAP api using the pyvmomi library"""

    def __init__(self, instance):
        self.host = instance['host']
        self.username = instance['username']
        self.password = instance['password']
        self.ssl_verify = is_affirmative(instance.get('ssl_verify', True))
        self.ssl_capath = instance.get('ssl_capath')
        self._conn = None
        self.smart_connect()

    def smart_connect(self):
        context = None
        if not self.ssl_verify:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
        elif self.ssl_capath:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(capath=self.ssl_capath)

        try:
            # Object returned by SmartConnect is a ServerInstance
            # https://www.vmware.com/support/developer/vc-sdk/visdk2xpubs/ReferenceGuide/vim.ServiceInstance.html
            conn = connect.SmartConnect(
                host=self.host,
                user=self.username,
                pwd=self.password,
                sslContext=context,
            )
            conn.CurrentTime()
        except Exception as e:
            err_msg = "Connection to {} failed: {}".format(ensure_unicode(self.host), e)
            raise ConnectionError(err_msg)

        self._conn = conn

    def get_connection(self):
        return self._conn

    @smart_retry
    def get_perf_counter_by_level(self, collection_level):
        return self._conn.content.perfManager.QueryPerfCounterByLevel(collection_level)

    @smart_retry
    def get_infrastructure(self):
        """Traverse the whole vSphere infrastructure and outputs dict mapping the mors to their properties.

        :return: {
            'vim.VirtualMachine-VM0': {
              'name': 'VM-0',
              ...
            }
            ...
        }
        """
        content = self._conn.content

        property_specs = []
        # Specify which attributes we want to retrieve per object
        for resource in ALL_RESOURCES:
            property_spec = vmodl.query.PropertyCollector.PropertySpec()
            property_spec.type = resource
            property_spec.pathSet = ["name", "parent", "customValue"]
            if resource == vim.VirtualMachine:
                property_spec.pathSet.append("runtime.powerState")
                property_spec.pathSet.append("runtime.host")
                property_spec.pathSet.append("guest.hostName")
            property_specs.append(property_spec)

        # Specify the attribute of the root object to traverse to obtain all the attributes
        traversal_spec = vmodl.query.PropertyCollector.TraversalSpec()
        traversal_spec.path = "view"
        traversal_spec.skip = False
        traversal_spec.type = vim.view.ContainerView

        retr_opts = vmodl.query.PropertyCollector.RetrieveOptions()
        # To limit the number of objects retrieved per call.
        # If batch_collector_size is 0, collect maximum number of objects.
        retr_opts.maxObjects = BATCH_COLLETOR_SIZE

        # Specify the root object from where we collect the rest of the objects
        obj_spec = vmodl.query.PropertyCollector.ObjectSpec()
        obj_spec.skip = True
        obj_spec.selectSet = [traversal_spec]

        # Create our filter spec from the above specs
        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.propSet = property_specs

        view_ref = content.viewManager.CreateContainerView(content.rootFolder, ALL_RESOURCES, True)
        try:
            obj_spec.obj = view_ref
            filter_spec.objectSet = [obj_spec]

            # Collect the objects and their properties
            res = content.propertyCollector.RetrievePropertiesEx([filter_spec], retr_opts)
            mors = res.objects
            # Results can be paginated
            while res.token is not None:
                res = content.propertyCollector.ContinueRetrievePropertiesEx(res.token)
                mors.extend(res.objects)
        finally:
            view_ref.Destroy()

        infrastructure_data = {
            mor.obj: {
                prop.name: prop.val for prop in mor.propSet
            }
            for mor in mors if mor.propSet
        }

        root_folder = self._conn.content.rootFolder
        infrastructure_data[root_folder] = {"name": root_folder.name, "parent": None}
        return infrastructure_data

    @smart_retry
    def query_metrics(self, query_specs):
        perf_manager = self._conn.content.perfManager
        return perf_manager.QueryPerf(query_specs)

    @smart_retry
    def get_new_events(self, start_time):
        event_manager = self._conn.content.eventManager
        query_filter = vim.event.EventFilterSpec()
        time_filter = vim.event.EventFilterSpec.ByTime(beginTime=start_time)
        query_filter.time = time_filter
        return event_manager.QueryEvents(query_filter)

    @smart_retry
    def get_latest_event_timestamp(self):
        event_manager = self._conn.content.eventManager
        return event_manager.latestEvent.createdTime