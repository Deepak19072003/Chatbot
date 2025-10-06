from typing import Dict
from .memory import ConversationManager
from .chatgpt import ChatGPTInterface


def print_memory_state(cm: ConversationManager) -> None:
    context = cm.get_context()
    print("\n📊 Current Memory State:")
    print(f"Total messages: {len(cm.messages)}")
    print(f"Recent messages (last {cm.short_context_size}): {len(context['recent'])}")
    print(f"Long-term facts: {len(context['facts'])}")
    print("\n🔍 Recent Context:")
    for i, msg in enumerate(context["recent"], 1):
        role_emoji = "👤" if msg["role"] == "user" else "🤖"
        print(f"{i}. {role_emoji} {msg['role']}: {msg['content'][:100]}...")
    if context["summary"]:
        print(f"\n📝 Summary of earlier messages:\n{context['summary']}")
    if context["facts"]:
        print(f"\n🧠 Long-term facts:")
        for fact in context["facts"]:
            print(f"  - {fact}")


def interactive_conversation() -> None:
    print("🤖 Data Analysis Copilot - Interactive Mode")
    print("Type 'quit' to exit, 'memory' to see current memory state")
    print("=" * 50)
    cm = ConversationManager(short_context_size=10)
    chatgpt = ChatGPTInterface()
    cm.add_message("system", "You are a helpful data analysis copilot. Provide concise, actionable insights.")
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            if user_input.lower() == "memory":
                print_memory_state(cm)
                continue
            if not user_input:
                continue
            cm.add_message("user", user_input)
            context: Dict = cm.get_context()
            messages = []
            if context["summary"]:
                messages.append({
                    "role": "system",
                    "content": f"Previous conversation summary:\n{context['summary']}\n\nUser facts: {context['facts']}",
                })
            for msg in context["recent"]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            response = chatgpt.get_response(messages)
            cm.add_message("assistant", response)
            print(f"🤖 Copilot: {response}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_run() -> None:
    cm = ConversationManager(short_context_size=10)
    scripted_messages = [
        ("user", "Hi, my name is Deepa. I'm working on a small sample of sales data."),
        ("assistant", "Hi Deepa! What analysis would you like to start with?"),
        ("user", "Assume we have sales by region for July–September; summarize revenue by region conceptually."),
        ("assistant", "I'll outline how to compute revenue by region and what insights to look for."),
        ("user", "I prefer results in tables with a concise narrative."),
        ("assistant", "I'll structure results as a table with key bullet insights."),
        ("user", "Drill down on APAC. Any anomalies we should watch for in July?"),
        ("assistant", "Watch for spikes due to one-off deals and promotions; verify data quality."),
        ("user", "Create a Q4 forecast using the last 8 quarters conceptually."),
        ("assistant", "We'll compare ARIMA baseline with a simple Prophet alternative and discuss trade-offs."),
        ("user", "Timezone for meetings is UTC+5:30."),
        ("assistant", "Noted. We'll schedule outputs relative to UTC+5:30."),
        ("user", "Propose charts for category-level growth and outline expected patterns."),
        ("assistant", "Recommend line and bar charts; annotate seasonal effects and product mix changes."),
        ("user", "Compare YoY growth for NA vs EU and note potential drivers."),
        ("assistant", "NA may outpace EU due to pricing and mix; verify with actual data when available."),
        ("user", "Summarize the main takeaways and propose a 6-slide outline."),
        ("assistant", "Drafted an outline with key insights and recommendations."),
        ("user", "Great. Prepare follow-up tasks for when data is available."),
        ("assistant", "Logged follow-ups: data validation, regional drill-downs, model benchmarking."),
        ("user", "Set a weekly reminder to revisit the analysis."),
        ("assistant", "Reminder scheduled weekly; we'll track open items and update findings."),
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
    print("  Letta: Supports structured core memory blocks to keep recent turns in context.")
    print("  Mem0: Focuses on persistent retrieval; recent-window trimming handled by your app (like this).")
    print("- Short-term memory summary (>N messages):")
    print("  Letta: Provides tools/prompts to maintain/update summaries in memory blocks.")
    print("  Mem0: You summarize with your app/LLM; Mem0 can store/retrieve summaries but not auto-summarize.")
    print("- Long-term memory (facts/preferences):")
    print("  Letta: Can persist user facts in dedicated blocks and update via memory tools.")
    print("  Mem0: Designed for long-term memory storage and retrieval keyed by user; strong fit.")


