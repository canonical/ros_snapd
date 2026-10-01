^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package ros2_snapd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.1 (2026-07-17)
------------------
* port branch configuration to lyrical
* ci: migrate jazzy workflow to GitHub ARM runner
* ci(promote): from candidate to stable
* ci(publish): publish on candidate
* fix: promote from edge to stable
  Since we publish on edge, we should promote from edge
* remove keepalive worklow
* fix(monthly): inherit secrets to reusable workflow
* fix(ci): remove snap-refresh-observe connection
* fix(snap): use only the new interface
* feat(snap): use the new ros-snapd-support interface
* add security policy
* use local monthly
* use jazzy ros2cli
* add choice for snap name
* update metadata, add monthly CI, add keepalive, add promote for ros2-snapd
* add git to build-packages to use git version, set publish channel to jazzy
* use git versioning
* update script to work with canonical workflows
* replace architectures with platforms (core24)
* update contact and website
* add jazzy
* doc(howto): add nav2 and rosbot links
* doc(How to use ros2 snapd): how to guide to show the usage of ros2 snapd with nav2
* fix(rate): use python sleep
* initial upload (humble)
