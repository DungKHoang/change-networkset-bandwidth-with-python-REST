

# Changing networkset bandwidth with Python and OneView REST API

The script updates exiting newtworkset bandwdith using Python and OneView REST API
The OneView python SDK (5.0) has no such function

## Prerequisites
The  script requires:
   * OneView python library 5.0 https://github.com/HewlettPackard/python-hpOneView/tree/release/5.0.0-beta
      See README of teh OneView python library for requirements for python version

## Environment

Your OneView environment should be at least at 4.00 level.


The networkset.csv contains the following fields:
   * networkset name  
   * typicalBandwidth
   * maximumBandwith

   Use the network.csv file as an example 

The oneview-config.json contains credential and IP address for OneView composer/appliance
   Use the oneview-config.json as an example 

## Syntax

### To change  ilo accounts

Before running the script, ensure that:
   * networkset.csv contains networkset names with their bandwdith
   * network sets are created in OneView
   * oneview_config.json is updated with information that match your environment


```

    .\updateNetworksetBandwidth.ps1 

```
