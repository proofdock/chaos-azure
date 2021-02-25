def healthy():
    return {
        "value": [
            {
                "id": "/subscriptions/00000000-000-0000-0000-000000000000/resourceGroups/rgname/providers/Microsoft"
                      ".Insights/metricAlerts/metricnamexx",
                "name": "Y3VycmVudFN0YXR1cw==",
                "type": "Microsoft.Insights/metricAlerts/status",
                "properties": {
                    "dimensions": {},
                    "status": "Healthy",
                    "timestamp": "2020-09-16T03:27:41.803534Z"
                }
            }
        ]
    }


def unhealthy():
    return {
        "value": [
            {
                "id": "/subscriptions/00000000-000-0000-0000-000000000000/resourceGroups/rgname/providers/Microsoft"
                      ".Insights/metricAlerts/metricnamexx",
                "name": "Y3VycmVudFN0YXR1cw==",
                "type": "Microsoft.Insights/metricAlerts/status",
                "properties": {
                    "dimensions": {},
                    "status": "xxx",
                    "timestamp": "2020-09-16T03:27:41.803534Z"
                }
            }
        ]
    }
