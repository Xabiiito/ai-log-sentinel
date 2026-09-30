import os
import ollama
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

LOG_FILE = "sample_auth.log"
OUTPUT_REPORT = "incident_report.md"

def analyze_logs_with_ai(log_content):
    """Sends suspicious system logs to Ollama (Mistral) acting as an expert SOC Analyst."""
    prompt = f"""
    Act as an expert Senior SOC (Security Operations Center) Analyst and Threat Intelligence specialist.
    Analyze the following system authentication logs for suspicious activities, brute-force attacks, unauthorized access attempts, or security anomalies.

    Logs to analyze:
    ```text
    {log_content}
    ```

    Provide a detailed incident response report including:
    1. Executive Summary of detected threats.
    2. Identification of suspicious IP addresses and attack vectors (e.g., SSH brute force).
    3. Severity level (High, Medium, Low) for each finding.
    4. Recommended remediation steps, firewall rules (e.g., iptables / fail2ban), or mitigation actions.
    """

    try:
        response = ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def main():
    console.print(Panel.fit("🛡️ Starting AI-Powered Log Sentinel (Ollama + Mistral)", style="bold cyan"))
    
    if not os.path.exists(LOG_FILE):
        console.print(f"[red]Error: Log file '{LOG_FILE}' not found.[/red]")
        return

    console.print(f"\n[yellow]🔍 Reading and parsing log file:[/yellow] {LOG_FILE}")
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        console.print(f"[red]Error reading log file: {e}[/red]")
        return

    console.print("[yellow]🤖 Sending logs to Local AI (Mistral) for Threat Intelligence analysis...[/yellow]")
    analysis_result = analyze_logs_with_ai(log_content)

    # Build report structure
    report_content = "# 🚨 AI Security Incident & Threat Intelligence Report\n\n"
    report_content += "Automated Log Sentinel analysis powered by Local AI.\n\n---\n\n"
    report_content += analysis_result

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report_content)

    console.print(f"\n[green]✅ Threat analysis completed successfully![/green]")
    console.print(f"[green]📄 Incident report generated at: {OUTPUT_REPORT}[/green]\n")

    console.print(Panel(Markdown(report_content), title="[bold blue]SOC Analysis Preview[/bold blue]", border_style="blue"))

if __name__ == "__main__":
    main()