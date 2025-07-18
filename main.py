from betting_tips import get_all_predictions

print("Generating betting tickets...\n")

sources = get_all_predictions()
for i, source in enumerate(sources):
    print(f"\n🎯 Source {i+1}")
    for match in source:
        print(f"• {match}") 
