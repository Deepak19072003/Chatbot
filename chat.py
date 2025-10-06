import datetime
from app.cli import interactive_conversation, demo_run


def demo():
    cm = ConversationManager(short_context_size=10)
    # Simulate a longer conversation; in a real app, messages would stream from UI/CLI
    scripted_messages = [
        ("user", "Hi, my name is DeepaK. I'm working on sales data for Q3."),
        ("assistant", "Hi Deepa! What analysis would you like to start with?"),
        (
            "user",
            "Load the dataset from /data/sales_q3.csv and give me a summary of revenue by region.",
        ),
        ("assistant", "Loaded dataset. Computing revenue by region and basic stats."),
        ("user", "I prefer results in tables with a concise narrative."),
        ("assistant", "Here is a table and a short narrative of key insights."),
        ("user", "Drill down on APAC. Any anomalies in July?"),
        ("assistant", "APAC shows a spike in July due to a one-off enterprise deal."),
        ("user", "Create a forecast for Q4 using last 8 quarters."),
        ("assistant", "Generating an ARIMA baseline and comparing with Prophet."),
        ("user", "Timezone for meetings is UTC+5:30."),
        ("assistant", "Noted. I will schedule outputs relative to UTC+5:30."),
        ("user", "Plot category-level growth and export charts as PNG."),
        ("assistant", "Charts generated and saved to /exports/q3/plots."),
        ("user", "Compare YoY growth for NA vs EU and annotate drivers."),
        ("assistant", "NA grew 12% YoY; EU grew 9%. Drivers: pricing and mix."),
        ("user", "Summarize the main takeaways and prepare a 6-slide deck."),
        ("assistant", "Drafted deck with key insights and recommendations."),
        ("user", "Great. Email it to the team and log a task for follow-ups."),
        # Extend beyond N=10 by adding additional steps typical of a data copilot
        ("assistant", "Email prepared; need SMTP credentials to send."),
        ("user", "Use the noreply account; credentials are in the vault."),
        ("assistant", "Authenticated. Sending emails to the team distribution list."),
        ("user", "Also share the dataset snapshot and model artifacts."),
        ("assistant", "Uploaded dataset snapshot and model pickles to /exports/q3/artifacts."),
        ("user", "Calculate contribution margins per product line for Q3."),
        ("assistant", "Computed margins; accessories underperform vs premium devices."),
        ("user", "Segment customers by RFM and attach cluster labels to the CRM."),
        ("assistant", "RFM clustering complete; labels exported to crm_rfm_labels.csv."),
        ("user", "Schedule a refresh job weekly until end of quarter."),
        ("assistant", "Created a cron job: Fridays 18:00 UTC+5:30; writes to /exports/q3/weekly."),
    ]

    for role, content in scripted_messages:
        cm.add_message(role, content)

    ctx = cm.get_context()
    print("=== Short-term context (last N messages) ===")
    for m in ctx["recent"]:
        print(f"{m['role']}: {m['content']}")
    print("\n=== Short-term summary of earlier messages ===")
    print(ctx["summary"])
    print("\n=== Long-term extracted facts/preferences ===")
    for fact in ctx["facts"]:
        print(fact)

    print("\n=== Library evaluation (Letta, Mem0) for memory tasks ===")
    print("- Trimming last N messages (N=10):")
    print(
        "  Letta: Supports structured core memory blocks to keep recent turns in context."
    )
    print(
        "  Mem0: Focuses on persistent retrieval; recent-window trimming handled by your app (like this)."
    )
    print("- Short-term memory summary (>N messages):")
    print(
        "  Letta: Provides tools/prompts to maintain/update summaries in memory blocks."
    )
    print(
        "  Mem0: You summarize with your app/LLM; Mem0 can store/retrieve summaries but not auto-summarize."
    )
    print("- Long-term memory (facts/preferences):")
    print(
        "  Letta: Can persist user facts in dedicated blocks and update via memory tools."
    )
    print(
        "  Mem0: Designed for long-term memory storage and retrieval keyed by user; strong fit."
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_conversation()
    else:
        print("Running demo mode. Use 'python chat.py interactive' for dynamic conversation.")
        demo_run()
