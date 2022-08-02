// META: title=RemoteContextHelper navigation helpers
// META: script=/common/dispatcher/dispatcher.js
// META: script=/common/get-host-info.sub.js
// META: script=/common/utils.js
// META: script=/resources/testharness.js
// META: script=/resources/testharnessreport.js
// META: script=/html/browsers/browsing-the-web/remote-context-helper/resources/remote-context-helper.js
// META: script=./resources/test-helper.js

'use strict';

promise_test(async t => {
  const rcHelper = new RemoteContextHelper();
  const rc1 = await rcHelper.addWindow();
  await assertSimplestScriptRuns(rc1);

  const rc2 = await rc1.navigateToNew();
  await assertSimplestScriptRuns(rc2);

  rc2.historyBack();
  await assertSimplestScriptRuns(rc1);

  rc1.historyForward();
  await assertSimplestScriptRuns(rc2);

  const rc3 = await rc2.navigateToNew();
  rc3.historyGo(-2);
  await assertSimplestScriptRuns(rc1);
});
