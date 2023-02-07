import re
import yaml
import templates.support_bundle as support_bundle

def convert_labels_to_seletors(labels):
    try:
        yml = yaml.load(labels.strip(), Loader=yaml.SafeLoader)
        return list(filter(None, [f'{key}={value}' for key, value in yml["metadata"]["labels"].items()]))
    except:
        if re.search(r".*:.*", labels):
            return [ l.replace(": ", "=").strip() for l in labels.split("\n")]
        else:
            return [ l.strip() for l in labels.split(",")]
        return []
        
        
def init_sb_template(synctax, input):
    noun_phrases = synctax["noun_phrases"]
    input_purpose = input
    troubleshoot_yaml = support_bundle.troubleshoot

    for e in noun_phrases:
        if re.search(r"support.+bundle", e):
            troubleshoot_yaml["kind"] = "SupportBundle"       
        if re.search(r"preflight", e):
            troubleshoot_yaml["kind"] = "Preflight"

    input_purpose = re.sub(r".*(bundle|preflight) yaml", "", input_purpose)

    return troubleshoot_yaml, input_purpose
    

def create_log_selectors(labels, namespace="default"):
    selectors = convert_labels_to_seletors(labels)
    log_collector["logs"]["namespace"] = [namespace]
    log_collector["logs"]["selector"] = selectors
    return log_collector

def create_log_selectors_from_svc_yaml(svc_yaml):
    try:
        log_collector = support_bundle.log_collector
        svc = yaml.load(svc_yaml.strip(), Loader=yaml.SafeLoader)
        print("\n\n========= openai generated yaml: =========\n")
        print(svc_yaml.strip())
        print("\n")
        namespace = svc["metadata"]["namespace"]
        selectors = list(filter(None, [f'{key}={value}' for key, value in svc["spec"]["selector"].items()]))
        log_collector["logs"]["namespace"] = namespace
        log_collector["logs"]["selector"] = selectors
        return log_collector
    except:
        return None

def create_cluster_pod_statuses_analyzer(pod_yaml):
    try:
        cluster_pod_statuses_analyzer = support_bundle.cluster_pod_statuses_analyzer
        pod = yaml.load(pod_yaml.strip(), Loader=yaml.SafeLoader)
        print("\n\n========= openai generated yaml: =========\n")
        print(pod_yaml.strip())
        print("\n")
        cluster_pod_statuses_analyzer["clusterPodStatuses"]["namespace"] = pod["metadata"]["namespace"]
        cluster_pod_statuses_analyzer["clusterPodStatuses"]["name"] = pod["metadata"]["name"]
        return cluster_pod_statuses_analyzer
    except:
        return None

def get_metric_labels(kubectl_cmd):
    print(kubectl_cmd)
    try:
        metric_labels = re.search(r"--metric-labels=(.*)", kubectl_cmd).group(1)
        return metric_labels
    except:
        return None

def split_to_stages(input):
    stages_input = input.split(";")
    return [input.strip() for input in stages_input]