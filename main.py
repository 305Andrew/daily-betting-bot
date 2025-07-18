from betting_tips import get_all_predictions

if __name__ == "__main__":
    print("⏳ Generating betting tickets...")
    tickets = get_all_predictions()
    for ticket in tickets:
        print("\n🎯 BETTING TICKET")
        for game in ticket:
            print(f" - {game}") 