import anthropic
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_5g_data(num_records=100, num_anomalies=8):
    """Generate synthetic 5G network KPI data with injected anomalies."""
    base_time = datetime(2026, 7, 15, 8, 0, 0)
    cell_ids = ["gNB-001", "gNB-002", "gNB-003", "gNB-004", "gNB-005"]

    # Build a list of measurements with realistic 5G KPI ranges
    data = []
    for i in range(num_records):
        timestamp = base_time + timedelta(minutes=15 * i)
        cell_id = random.choice(cell_ids)
        rsrp = random.gauss(-85, 8)
        rsrq = random.gauss(-11, 3)
        sinr = random.gauss(15, 5)
        throughput_dl = random.gauss(150, 40)
        latency = random.gauss(8, 2)
        data.append({
            "timestamp": timestamp,
            "cell_id": cell_id,
            "rsrp_dbm": round(rsrp, 1),
            "rsrq_db": round(rsrq, 1),
            "sinr_db": round(sinr, 1),
            "throughput_dl_mbps": round(max(throughput_dl, 1), 1),
            "latency_ms": round(max(latency, 0.5), 1),
        })

    df = pd.DataFrame(data)
        # Inject anomalies: coverage holes, interference, congestion
    anomaly_indices = random.sample(range(num_records), num_anomalies)
    for idx in anomaly_indices:
        anomaly_type = random.choice(["coverage", "interference", "congestion"])
        if anomaly_type == "coverage":
            df.at[idx, "rsrp_dbm"] = round(random.uniform(-115, -105), 1)
            df.at[idx, "throughput_dl_mbps"] = round(random.uniform(5, 20), 1)
        elif anomaly_type == "interference":
            df.at[idx, "sinr_db"] = round(random.uniform(-5, 2), 1)
            df.at[idx, "rsrq_db"] = round(random.uniform(-22, -18), 1)
        elif anomaly_type == "congestion":
            df.at[idx, "latency_ms"] = round(random.uniform(25, 50), 1)
            df.at[idx, "throughput_dl_mbps"] = round(random.uniform(10, 30), 1)

    return df

def detect_anomalies(df, threshold=2.0):
    """Detect anomalies using z-score method on numeric KPI columns."""
    kpi_columns = ["rsrp_dbm", "rsrq_db", "sinr_db", "throughput_dl_mbps", "latency_ms"]

    anomalies = pd.DataFrame(index=df.index)
    anomalies["is_anomaly"] = False
    anomalies["anomaly_details"] = ""

    for col in kpi_columns:
        mean = df[col].mean()
        std = df[col].std()
        z_scores = (df[col] - mean) / std

        flagged = z_scores.abs() > threshold

        for idx in df[flagged].index:
            anomalies.at[idx, "is_anomaly"] = True
            detail = f"{col}={df.at[idx, col]} (z={z_scores[idx]:.1f})"
            if anomalies.at[idx, "anomaly_details"]:
                anomalies.at[idx, "anomaly_details"] += "; " + detail
            else:
                anomalies.at[idx, "anomaly_details"] = detail

    return anomalies

def calculate_cell_scores(df, anomalies):
    """Calculate a health score (0-100) for each cell based on anomaly count and severity."""
    anomaly_mask = anomalies["is_anomaly"]
    anomaly_records = df[anomaly_mask].copy()
    anomaly_records["anomaly_details"] = anomalies.loc[anomaly_mask, "anomaly_details"].values

    cell_ids = df["cell_id"].unique()
    scores = {}

    for cell_id in cell_ids:
        cell_anomalies = anomaly_records[anomaly_records["cell_id"] == cell_id]
        score = 100

        for _, row in cell_anomalies.iterrows():
            if row["rsrp_dbm"] < -110:
                score -= 20
            elif row["rsrp_dbm"] < -100:
                score -= 10
            if row["sinr_db"] < 0:
                score -= 20
            elif row["sinr_db"] < 5:
                score -= 10
            if row["latency_ms"] > 25:
                score -= 15
            elif row["latency_ms"] > 15:
                score -= 8
            if row["throughput_dl_mbps"] < 20:
                score -= 15
            elif row["throughput_dl_mbps"] < 50:
                score -= 8

        scores[cell_id] = max(score, 0)
        
    scores_df = pd.DataFrame(
        [{"cell_id": k, "health_score": v} for k, v in scores.items()]
    )
    scores_df = scores_df.sort_values("health_score", ascending=True).reset_index(drop=True)

    return scores_df

def get_cell_recommendation(scores_df):
    """Ask Claude to provide a prioritized recommendation based on cell scores."""
    client = anthropic.Anthropic()

    scorecard_text = scores_df.to_string(index=False)

    prompt = f"""You are a 5G network operations center (NOC) engineer AI assistant.
    Below is a health scorecard for cell sites in a 5G NR network. Each cell has a score from 0 (critical) to 100 (perfect health).
    
    Cell Health Scorecard:
    {scorecard_text}
    
    Based on these scores:
    1. Identify the highest-priority cell that needs immediate attention
    2. Recommend one of these actions for the priority cell:
        - Dispatch field engineer (for hardware/coverage issues)
        - Adjust antenna parameters remotely (for tilt/power optimization)
        - Escalate to RF planning team (for systemic interference or capacity issues)
    3. Briefly explain your reasoning (2-3 sentences)
    4. For cells scoring above 80, confirm they need no immediate action
    Keep your response concise and actionable."""

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    # Safely extract and combine only the text blocks, ignoring thinking blocks
    text_content = [block.text for block in message.content if block.type == "text"]
    return "".join(text_content)

def analyze_with_claude(df, anomalies):
    """Send detected anomalies to Claude for telecom-specific diagnosis."""
    client = anthropic.Anthropic()

    # Filter the full DataFrame to only anomalous rows
    anomaly_mask = anomalies["is_anomaly"]
    anomaly_records = df[anomaly_mask].copy()
    anomaly_records["anomaly_details"] = anomalies.loc[anomaly_mask, "anomaly_details"].values

    if anomaly_records.empty:
        return "No anomalies detected in the current dataset."

    # Convert anomaly records to a readable string
    anomaly_summary = anomaly_records.to_string(index=False)

    # Send a basic prompt with the data
    prompt = f"""You are a 5G network operations center (NOC) engineer AI assistant.
    Analyze the following anomalous KPI measurements from a 5G NR network and provide a structured diagnostic report.
    Reference thresholds for healthy 5G NR performance:
    - SS-RSRP: >= -90 dBm (Good), >= -80 dBm (Excellent), < -100 dBm (Weak), < -110 dBm (Critical)
    - SS-RSRQ: >= -10 dB (Excellent), -10 to -15 dB (Good), < -20 dB (Severely degraded)
    - SS-SINR: >= 20 dB (Excellent), 13-20 dB (Good), 0-13 dB (Acceptable), < 0 dB (Critical)
    - DL Throughput: >= 100 Mbps (mid-band target)
    - Latency: <= 10 ms (eMBB target)
    
    Anomalous measurements detected:
    {anomaly_summary}
    
    For each anomaly, provide:
    1. Severity (Critical / Major / Minor)
    2. Probable root cause (coverage hole, interference/pilot pollution, congestion, handover issue, or equipment fault)
    3. Affected KPIs and their relationship
    4. Recommended action for the NOC team
    
    End with a summary of overall network health and priority actions."""

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    # Safely extract and combine only the text blocks, ignoring thinking blocks
    text_content = [block.text for block in message.content if block.type == "text"]
    return "".join(text_content)

def main():
    print("=" * 60)
    print("  5G Network Anomaly Detection Agent")
    print("  Powered by Claude AI")
    print("=" * 60)
    print()

    # Generate synthetic 5G KPI data
    print("[1/4] Generating 5G network KPI data...")
    df = generate_5g_data(num_records=100, num_anomalies=8)
    print(f"  Generated {len(df)} measurements across {df['cell_id'].nunique()} cells")
    print(f"  Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print()

    print("[2/4] Running anomaly detection (z-score threshold: 2.0)...")
    anomalies = detect_anomalies(df, threshold=2.0)
    num_anomalies_found = anomalies["is_anomaly"].sum()
    print(f"  Detected {num_anomalies_found} anomalous measurements")
    print()

    if num_anomalies_found > 0:
        anomaly_mask = anomalies["is_anomaly"]
        print("  Flagged records:")
        flagged_display = df[anomaly_mask][["timestamp", "cell_id", "rsrp_dbm", "sinr_db", "throughput_dl_mbps", "latency_ms"]].copy()
        print(flagged_display.to_string(index=False))
        print()

    # Send anomalies to Claude for interpretation
    print("[3/4] Sending anomalies to Claude for diagnosis...")
    print()
    report = analyze_with_claude(df, anomalies)
    print("=" * 60)
    print("  DIAGNOSTIC REPORT")
    print("=" * 60)
    print()
    print(report)
    print()

    print("[4/4] Calculating per-cell health scorecard...")
    print()
    scores_df = calculate_cell_scores(df, anomalies)
    print("  Cell Health Rankings (worst to best):")
    print(scores_df.to_string(index=False))
    print()

    print("  Getting prioritized recommendation from Claude...")
    print()
    recommendation = get_cell_recommendation(scores_df)
    print("=" * 60)
    print("  PRIORITY RECOMMENDATION")
    print("=" * 60)
    print()
    print(recommendation)

if __name__ == "__main__":
    main()