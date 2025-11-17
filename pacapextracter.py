import pyshark
import pandas as pd
from scapy.all import rdpcap, TCP
import os

flows = {}

def get_flow_key(pkt):
    try:
        src = pkt.ip.src
        dst = pkt.ip.dst
        src_p = pkt[pkt.transport_layer].srcport
        dst_p = pkt[pkt.transport_layer].dstport
        proto = pkt.transport_layer
        return f"{src}-{dst}-{src_p}-{dst_p}-{proto}"
    except:
        return None


def update_flow(flow_key, pkt, scapy_pkt):
    flow = flows.setdefault(flow_key, {
        "timestamps": [],
        "fwd_pkt_count": 0,
        "bwd_pkt_count": 0,
        "fwd_bytes": 0,
        "bwd_bytes": 0,
        "pkt_lengths": [],
        "iat_list": [],
        "syn_count": 0,
        "ack_count": 0,
        "src_port": 0,
        "dst_port": 0,
        "protocol": 0
    })

    ts = float(pkt.sniff_timestamp)
    flow["timestamps"].append(ts)

    length = int(pkt.length)
    flow["pkt_lengths"].append(length)

    try:
        flow["src_port"] = int(pkt[pkt.transport_layer].srcport)
        flow["dst_port"] = int(pkt[pkt.transport_layer].dstport)
        flow["protocol"] = 6 if pkt.transport_layer == "TCP" else 17
    except:
        pass

    try:
        src_ip = pkt.ip.src
        if flow_key.startswith(src_ip):
            flow["fwd_pkt_count"] += 1
            flow["fwd_bytes"] += length
        else:
            flow["bwd_pkt_count"] += 1
            flow["bwd_bytes"] += length
    except:
        return

    if scapy_pkt.haslayer(TCP):
        tcp = scapy_pkt[TCP]
        if tcp.flags & 0x02:
            flow["syn_count"] += 1
        if tcp.flags & 0x10:
            flow["ack_count"] += 1


def finalize_flows():
    rows = []

    for key, f in flows.items():
        ts = f["timestamps"]
        duration = max(ts) - min(ts) if len(ts) > 1 else 0

        iats = []
        for i in range(1, len(ts)):
            iats.append(ts[i] - ts[i - 1])

        rows.append({
            "flow_duration": duration,
            "forward_packets": f["fwd_pkt_count"],
            "backward_packets": f["bwd_pkt_count"],
            "forward_bytes": f["fwd_bytes"],
            "backward_bytes": f["bwd_bytes"],
            "packet_length_mean": sum(f["pkt_lengths"]) / len(f["pkt_lengths"]) if f["pkt_lengths"] else 0,
            "packet_length_std": pd.Series(f["pkt_lengths"]).std() if len(f["pkt_lengths"]) > 1 else 0,
            "iat_mean": sum(iats) / len(iats) if len(iats) else 0,
            "iat_std": pd.Series(iats).std() if len(iats) > 1 else 0,
            "syn_count": f["syn_count"],
            "ack_count": f["ack_count"],
            "src_port": f["src_port"],
            "dst_port": f["dst_port"],
            "protocol": f["protocol"]
        })

    return pd.DataFrame(rows)


def extract(pcap_path):
    print(f"\n[+] Reading PCAP: {pcap_path}\n")

    cap = pyshark.FileCapture(pcap_path, keep_packets=False)
    scapy_packets = rdpcap(pcap_path)

    for pkt, scapy_pkt in zip(cap, scapy_packets):
        key = get_flow_key(pkt)
        if key:
            update_flow(key, pkt, scapy_pkt)

    df = finalize_flows()

    # auto CSV name
    base = os.path.basename(pcap_path).split('.')[0]
    csv_name = f"{base}_features.csv"

    df.to_csv(csv_name, index=False)

    print(f"[+] Extracted {len(df)} flows")
    print(f"[+] Saved CSV at: {csv_name}\n")


if __name__ == "__main__":
    print("=== Dark Web Traffic Feature Extractor ===\n")
    
    pcap_path = input("Enter the PCAP/PCAPNG file path: ").strip()

    if not os.path.exists(pcap_path):
        print("\n❌ Error: File not found!")
        exit()

    extract(pcap_path)
    print("✔ Done!")

