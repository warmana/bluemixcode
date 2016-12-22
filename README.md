# bluemixcode

A simple repository,
making it easy to create and test sample code for accessing IBM Bluemix services.

## Publishing to Bluemix

1.  Download and install the [Bluemix Command Line interface](http://clis.ng.bluemix.net/ui/home.html).
2.  Download and install the [Cloud Foundry Command Line interface](https://github.com/cloudfoundry/cli/releases).
    Many Linux OS distributions have Cloud Foundry available in their application repositories.
    As long as you CF version is 6.11 or better,
    it should work with Bluemix.
3.  Download the Starter Code package for your application.
    This includes a number of starter and configuration files that you can modify for your application.
4.  Connect to Bluemix:
    `bluemix api https://api.ng.bluemix.net`
5.  Log in to Bluemix:
    `bluemix login -u Adrian.Warman@uk.ibm.com -o Adrian.Warman@uk.ibm.com -s dev`
6.  Deploy the app to Bluemix:
    `cf push "CloudantPython"`
