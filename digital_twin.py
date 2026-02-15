import pandas as pd

def load_event_log(file_path):
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["case_id", "timestamp"])
    return df


def build_digital_twin(df):
    digital_twin = []

    for case_id, group in df.groupby("case_id"):

        start_time = group.iloc[0]["timestamp"]
        last_event = group.iloc[-1]

        total_duration = (last_event["timestamp"] - start_time).total_seconds() / 3600

        variant = " -> ".join(group["activity"].tolist())

        digital_twin.append({
            "Case ID": case_id,
            "Current Activity": last_event["activity"],
            "Total Duration (hrs)": round(total_duration, 2),
            "Completed": last_event["activity"] == "Order Delivered",
            "Delayed (>24 hrs)": total_duration > 24,
            "Variant": variant
        })

    return pd.DataFrame(digital_twin)


def process_summary(twin_df):
    print("\n=== PROCESS SUMMARY ===\n")
    print(f"Total Cases: {len(twin_df)}")
    print(f"Completed Cases: {twin_df['Completed'].sum()}")
    print(f"Incomplete Cases: {len(twin_df) - twin_df['Completed'].sum()}")
    print(f"Delayed Cases (>24 hrs): {twin_df['Delayed (>24 hrs)'].sum()}")

    print("\nTop 3 Process Variants:")
    print(twin_df["Variant"].value_counts().head(3))


if __name__ == "__main__":

    df = load_event_log("event_log.csv")
    twin_df = build_digital_twin(df)

    print("\n=== DIGITAL TWIN SNAPSHOT (First 10 Cases) ===\n")
    print(twin_df.head(10).to_string(index=False))

    process_summary(twin_df)

    # Save full output to CSV
    twin_df.to_csv("digital_twin_output.csv", index=False)
    print("\nFull Digital Twin results saved to digital_twin_output.csv")
