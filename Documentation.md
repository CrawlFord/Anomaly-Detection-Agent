# 5G Network Anomaly Detection Agent

**Project Link:** [View Project](https://nextwork.ai/projects/80e6ffec-6938-482c-ab59-89109492e21c)

**Author:** Torobong Andrew-Udoh  
**Email:** tandrewudoh@gmail.com
<img src="https://www.magnific.com/free-photos-vectors/gmail" alt="email adress" width="50" />

---

![Image](https://nextwork.ai/vibrant_purple_swift_sow/uploads/80e6ffec-6938-482c-ab59-89109492e21c_e4cf62ov)

## Building a 5G Network Operations Agent

### Project goals and telecom relevance

In this project, I'm building a Python agent that automatically detects anomalies in 5G network data and uses Claude to generate structured diagnostic reports that a network engineer could act on so that I can gain hands-on experience calling Claude's API from Python, including authentication, message handling, and reading structured responses.

## Setting Up the Development Environment

### Environment and dependencies

In this step, I'm setting up a Python virtual environment then configuring an API key so that the agent can talk to Claude.

![Image](https://nextwork.ai/vibrant_purple_swift_sow/uploads/80e6ffec-6938-482c-ab59-89109492e21c_qa6ir6zm)

## Generating Realistic 5G Network KPI Data

### Synthetic data generation approach

In this step, I'm generating synthetic data that follows real 5G parameter ranges so that I can simulate what a Network Operations Center (NOC) monitoring system would see.

![Image](https://nextwork.ai/vibrant_purple_swift_sow/uploads/80e6ffec-6938-482c-ab59-89109492e21c_80mni8rr)

### Understanding the five 5G KPIs

The five KPIs are timestamp, cell_id, rsrp_dbm, rsrq_db, sinr_db, throughput_dl_mbps, and latency_ms and A NOC engineer uses these to scan for anomalies in data.

## Detecting Anomalies with Statistical Z-Scores

### Automated anomaly detection logic

In this step, I'm building a z-score based anomlay detection function so that I can display a table of flagged anomalous records with details.

![Image](https://nextwork.ai/vibrant_purple_swift_sow/uploads/80e6ffec-6938-482c-ab59-89109492e21c_r35asnse)

### Interpreting z-score results

A z-score of -3.4 means the value is 3.4 standard deviations below the mean, which indicates an extremely weak signal and a significant network anomaly

## Integrating Claude for AI-Powered Diagnosis

### Connecting the Claude API

In this step, I'm connecting my agent to Claude API so that the agent can intepret the anomaly data and produce a human-readable diagnosis.

![Image](https://nextwork.ai/vibrant_purple_swift_sow/uploads/80e6ffec-6938-482c-ab59-89109492e21c_wed2s0np)

### Identifying gaps in generic AI responses

I noticed that Claude's response lacks formal severity classifications (like Critical, Major, and Minor) for each flagged event, and it does not reference standardized 3GPP 5G NR thresholds (such as specific dBm or dB values) to justify its diagnosis. A NOC engineer would need exact severity levels to prioritize their tickets, concrete reference standards to verify the diagnosis, and a machine-readable format (like JSON) to automatically route alerts to tools like ServiceNow or Jira.

## Engineering a Telecom-Specific Diagnostic Report

### Prompt engineering for domain expertise

In this step, I'm replacing the generic response Claude gave by giving it the 5G NR reference threshold, a NOC engineer persona, and a required output structure so that the agent produces an actionable diagnostic tool

### Impact of structured prompting on output quality

The generic response was a simple list of observations about the raw numbers without any network context or prioritization, but the structured report includes clear severity levels (Critical/Major/Minor), probable root causes (like coverage holes or interference) mapped to 3GPP standards, and actionable recommendations for the NOC team.

## Per-Cell Health Scorecard and Priority Recommendations

![Image](https://nextwork.ai/vibrant_purple_swift_sow/uploads/80e6ffec-6938-482c-ab59-89109492e21c_qrj1g0da)

### Scoring formula and AI-driven prioritization

In this project extension, the scoring formula deducts points based on the severity and type of KPI anomalies detected (such as deducting 20 points for critical RSRP below -110 dBm or critical SINR below 0 dB, and 15 points for high latency or low throughput). Claude recommended [Pasted Recommendation] for cell [Your Lowest Scoring Cell ID, e.g., Cell_3] because this site had the lowest health score due to severe [e.g., coverage or interference] issues that violated key 3GPP thresholds.

## Reflections and Key Takeaways

### Tools and concepts mastered

The key tools I used include Python as my core programming language, pandas for structuring and manipulating complex network telemetry data, the Anthropic SDK to connect my backend to Claude, and an isolated virtual environment in VS Code to manage dependencies securely. Key concepts I learnt include statistical anomaly detection using Z-score calculations to automatically flag metric deviations, 5G performance benchmarks based on 3GPP thresholds (such as RSRP, RSRQ, and SINR), advanced prompt engineering using system personas and structured outputs to convert raw numbers into human-readable engineering reports, API response deserialization (specifically how to handle and filter ThinkingBlock and TextBlock objects), and how to aggregate distributed telemetry data to build a prioritized NOC resource-allocation scorecard.


### Time and challenges

This project took me approximately 75 minutes. The most challenging part was connecting the API key into my virtual environment that allowed for communication to Claude.

I did this project today to learn how to build an end-to-end intelligent AI agent that combines statistical anomaly detection (Z-scores) with advanced LLM prompt engineering to automate complex 5G network troubleshooting and resource prioritization. Another skill I want to learn is how to deploy this agentic workflow as an interactive dashboard using Gradio on Hugging Face Spaces, and how to swap the statistical Z-score detector with a real-time deep learning classifier (such as a 1D CNN) to handle highly complex signal quality anomalies dynamically.

---

[View this project](https://nextwork.ai/projects/80e6ffec-6938-482c-ab59-89109492e21c)*
