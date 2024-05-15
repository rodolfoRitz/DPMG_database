---
title: "BiDirectional Functionality"
linkTitle: "BiDirectional"
weight: 16
aliases: [
"/documentation/pt-br/webdriver/bidi_apis/",
"/pt-br/documentation/webdriver/bidi_apis/",
"/pt-br/documentation/webdriver/bidirectional/bidi_api_remotewebdriver"
]
---

{{% pageinfo color="warning" %}}
<p class="lead">
   <i class="fas fa-language d-4"></i>
   Page being translated from
   English to Portuguese. Do you speak Portuguese? Help us to translate
   it by sending us pull requests!
</p>
{{% /pageinfo %}}

Selenium is working with browser vendors to create the
[WebDriver BiDirectional Protocol](https://w3c.github.io/webdriver-bidi/)
as a means to provide a stable, cross-browser API that uses the bidirectional
functionality useful for both browser automation generally and testing specifically.
Before now, users seeking this functionality have had to rely on
with all of its frustrations and limitations.

The traditional WebDriver model of strict request/response commands will be supplemented
with the ability to stream events from the user agent to the controlling software via WebSockets,
better matching the evented nature of the browser DOM.

As it is not a good idea to tie your tests to a specific version of any browser, the
Selenium project recommends using WebDriver BiDi wherever possible.

While the specification is in works, the browser vendors are parallely implementing
the [WebDriver BiDirectional Protocol](https://w3c.github.io/webdriver-bidi/).
Refer [web-platform-tests dashboard](https://wpt.fyi/results/webdriver/tests/bidi?label=experimental&label=master&aligned&view=subtest)
to see how far along the browser vendors are.
Selenium is trying to keep up with the browser vendors and has started implementing W3C BiDi APIs.
The goal is to ensure APIs are W3C compliant and uniform among the different language bindings.

However, until the specification and corresponding Selenium implementation is complete there are many useful things that
CDP offers. Selenium offers some useful helper classes that use CDP.