
troubleshoot = {
  "apiVersion": "troubleshoot.sh/v1beta2",
  "kind": "",
  "metadata":
    {"name": ""},
  "spec": {},
}

log_collector = {
  "logs": {
    "selector": [],
    "namespace": "",
  },
}

cluster_pod_statuses_analyzer = {
  "clusterPodStatuses": {
    "name": "",
    "namespace": [],
    "outcomes": [
        {
            "fail": {
                "when": "== CrashLoopBackOff",
                "message": "Pod {{ .Namespace }}/{{ .Name }} is in a CrashLoopBackOff state.",
            },
            "fail": {
                "when": "!= Healthy",
                "message": "Pod {{ .Namespace }}/{{ .Name }} is unhealthy with a status of {{ .Status.Reason }}.",
            }
        },
    ]
  },
}