# CHANGELOG - sqlserver

## 1.14.0 / 2019-10-11

* [Added] Upgrade pywin32 to 225. See [#4563](https://github.com/DataDog/integrations-core/pull/4563).

## 1.13.0 / 2019-07-13

* [Added] Allow SQLNCLI11 provider in SQL server. See [#4097](https://github.com/DataDog/integrations-core/pull/4097).

## 1.12.0 / 2019-07-08

* [Added] Upgrade dependencies for Python 3.7 binary wheels. See [#4030](https://github.com/DataDog/integrations-core/pull/4030).

## 1.11.0 / 2019-05-14

* [Added] Adhere to code style. See [#3567](https://github.com/DataDog/integrations-core/pull/3567).

## 1.10.1 / 2019-04-04

* [Fixed] Don't ship `pyodbc` on macOS as SQLServer integration is not shipped on macOS. See [#3461](https://github.com/DataDog/integrations-core/pull/3461).

## 1.10.0 / 2019-03-29

* [Added] Add custom instance tags to storedproc metrics. See [#3237](https://github.com/DataDog/integrations-core/pull/3237).
* [Fixed] Use execute instead of callproc if using (py)odbc. See [#3236](https://github.com/DataDog/integrations-core/pull/3236).

## 1.9.0 / 2019-02-18

* [Added] Support Python 3. See [#3027](https://github.com/DataDog/integrations-core/pull/3027).

## 1.8.1 / 2019-01-04

* [Fixed] Bump pyodbc for python3.7 compatibility. See [#2801][1].

## 1.8.0 / 2018-11-30

* [Added] Add linux as supported OS. See [#2614][2].
* [Fixed] Additional debug logging when calling a stored procedure. See [#2151][3].
* [Fixed] Use raw string literals when \ is present. See [#2465][4].

## 1.7.0 / 2018-10-12

* [Added] Pin pywin32 dependency. See [#2322][5].

## 1.6.0 / 2018-09-04

* [Added] Support higher query granularity. See [#2017][6].
* [Added] Add ability to support (via configuration flag) the newer ADO provider. See [#1673][7].
* [Fixed] Stop leaking db password when a connection is not in the pool. See [#2031][8].
* [Fixed] Bump pyro4 and serpent dependencies. See [#2007][9].
* [Fixed] Fix for case sensitivity in the `proc_type_mapping` dict.. See [#1860][10].
* [Fixed] Add data files to the wheel package. See [#1727][11].

## 1.5.0 / 2018-06-20

* [Added] support object_name metric identifiers. See [#1679][12].

## 1.4.0 / 2018-05-11

* [FEATURE] Add custom tag support for service checks.

## 1.3.0 / 2018-02-13

* [IMPROVEMENT] Allow custom connection string to connect. See [#1068][13].

## 1.2.1 / 2018-01-10

* [BUGFIX] Allows metric collection from all instances in custom query. See [#959][14].
* [BUGFIX] Repair reporting of stats from sys.dm_os_wait_stats. See [#975][15].

## 1.2.0 / 2017-10-10

* [FEATURE] single bulk query of all of metrics, then filter locally. See [#573][16].

## 1.1.0 / 2017-07-18

* [FEATURE] Allow calling custom proc to return metrics, and improve transaction handling. See [#357][17] and [#456][18], thanks [@rlaveycal][19]
* [SANITY] Fix yaml example file spacing. See [#342][20], thanks [@themsquared][21]

## 1.0.0 / 2017-03-22

* [FEATURE] adds sqlserver integration.

<!--- The following link definition list is generated by PimpMyChangelog --->
[1]: https://github.com/DataDog/integrations-core/pull/2801
[2]: https://github.com/DataDog/integrations-core/pull/2614
[3]: https://github.com/DataDog/integrations-core/pull/2151
[4]: https://github.com/DataDog/integrations-core/pull/2465
[5]: https://github.com/DataDog/integrations-core/pull/2322
[6]: https://github.com/DataDog/integrations-core/pull/2017
[7]: https://github.com/DataDog/integrations-core/pull/1673
[8]: https://github.com/DataDog/integrations-core/pull/2031
[9]: https://github.com/DataDog/integrations-core/pull/2007
[10]: https://github.com/DataDog/integrations-core/pull/1860
[11]: https://github.com/DataDog/integrations-core/pull/1727
[12]: https://github.com/DataDog/integrations-core/pull/1679
[13]: https://github.com/DataDog/integrations-core/pull/1065
[14]: https://github.com/DataDog/integrations-core/issues/959
[15]: https://github.com/DataDog/integrations-core/pull/975
[16]: https://github.com/DataDog/integrations-core/issues/573
[17]: https://github.com/DataDog/integrations-core/issues/357
[18]: https://github.com/DataDog/integrations-core/issues/456
[19]: https://github.com/rlaveycal
[20]: https://github.com/DataDog/integrations-core/issues/342
[21]: https://github.com/themsquared