import streamlit as st
import random
import time

# --- 1. SETUP & VARIABLES (Always run first) ---
st.set_page_config(page_title="My first App", page_icon="🥹")

# Initialize "Backpack" (Session State)
if 'pizza_points' not in st.session_state: st.session_state.pizza_points = 0
if 'multiplier' not in st.session_state: st.session_state.multiplier = 1

# Shop Upgrades
if 'oven_level' not in st.session_state: st.session_state.oven_level = 1
if 'golden_spade' not in st.session_state: st.session_state.golden_spade = False
if 'luck_charm' not in st.session_state: st.session_state.luck_charm = False
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# Event Flags
if 'alien_visited' not in st.session_state: st.session_state.alien_visited = False
if 'time_travel_visited' not in st.session_state: st.session_state.time_travel_visited = False


# --- 2. MAIN NAVIGATION (SIDEBAR) ---
st.sidebar.title("Choose section")

# The Main Category Selector
section = st.sidebar.selectbox(
    "Go to:", 
    ["Home", "Pizzeria" , "Mood-Checker", "🎮Mini-Games", "🛠️ Tools"]
)

# Always show points in Sidebar
st.sidebar.markdown("---")
st.sidebar.metric("Total XP ⭐", st.session_state.pizza_points)

if st.session_state.multiplier > 1:
    st.sidebar.warning(f"⚡ {st.session_state.multiplier}X BOOST ACTIVE!")


# ==========================================
#  SECTION 1: HOME
# ==========================================
if section == "Home":
    st.title('My first App!')
    st.write("Welcome! Use the menu on your left to navigate.")
    
    
    if st.button('Click me'):
        st.write('Surprise! 🎉')
        st.balloons()



# ==========================================
#  SECTION 2: PIZZERIA (The Main Game)
# ==========================================
elif section == "Pizzeria":
    st.title("👨‍🍳 My Pizzeria")

    # --- SIDEBAR SHOP (Only visible here) ---
    st.sidebar.header("🛒 Upgrade Shop")
    
    # Oven
    oven_cost = st.session_state.oven_level * 500
    st.sidebar.write(f"Oven Level: {st.session_state.oven_level}")
    if st.sidebar.button(f"Upgrade Oven ({oven_cost} ⭐)"):
        if st.session_state.pizza_points >= oven_cost:
            st.session_state.pizza_points -= oven_cost
            st.session_state.oven_level += 1
            st.rerun()
        else:
            st.sidebar.error("Not enough points!")

    # Golden Spade
    if not st.session_state.golden_spade:
        if st.sidebar.button("Golden Spade (2000 ⭐)"):
            if st.session_state.pizza_points >= 2000:
                st.session_state.pizza_points -= 2000
                st.session_state.golden_spade = True
                st.rerun()
            else:
                st.sidebar.error("Not enough points!")
    else:
        st.sidebar.success("✅ Golden Spade Owned!")

    # Luck Charm
    if not st.session_state.luck_charm:
        if st.sidebar.button("Luck Charm (1500 ⭐)"):
            if st.session_state.pizza_points >= 1500:
                st.session_state.pizza_points -= 1500
                st.session_state.luck_charm = True
                st.rerun()
            else:
                st.sidebar.error("Not enough points!")
    else:
        st.sidebar.info("🍀 Luck Charm Owned!")

    # --- BAKING SECTION ---
    st.write("Each ingredient gives you **10 points** (+ bonuses)!")
    
    base = st.selectbox("Choose your crust:", ["Regular", "Whole grain", "Gluten-free", "Golden Crust (VIP)"])
    toppings = st.multiselect(
        "Select your toppings:",
        ["Cheese", "Ham", "Pepperoni", "Pineapple", "Mushroom", "Bacon", "BBQ", "Prawns", "Potato", "Extra Cheese"]
    )

    if st.button("Bake my Pizza!"):
        if toppings:
            base_points = len(toppings) * 10
            oven_bonus = st.session_state.oven_level * 10
            crust_bonus = 50 if base == "Golden Crust (VIP)" else 0
            spade_mult = 1.5 if st.session_state.golden_spade else 1.0
            
            total_score = int((base_points + oven_bonus + crust_bonus) * spade_mult * st.session_state.multiplier)
            
            st.session_state.pizza_points += total_score
            st.success(f"Yum! You earned {total_score} ⭐")
            
            if st.session_state.multiplier > 1: st.info("Bob's 2x Boost Applied!")
            if st.session_state.golden_spade: st.info("Golden Spade Bonus Applied!")
        else:
            st.warning("You can't bake an empty pizza!")

    # --- EVENTS & RANKS (Ordered from Highest to Lowest) ---
    
    # 1. GOD MODE (1,000,000)
    if st.session_state.pizza_points >= 1000000:
        if 'god_mode_toast' not in st.session_state:
            st.toast("WOW! You are the god of pizzas!", icon="🍕")
            st.session_state.god_mode_toast = True
        st.write("### 👑 GOD OF PIZZA!!!!!")
        st.write("You have reached the ultimate level!")
        if st.button("Ascend and Reset Game"):
            st.session_state.pizza_points = 0
            del st.session_state.god_mode_toast 
            st.rerun()
        st.stop()

    # 2. TIME TRAVEL (380,000)
    elif st.session_state.pizza_points >= 380000 and not st.session_state.time_travel_visited:
        st.toast("Uh oh, what have you done?", icon="🌀")
        time.sleep(1)
        st.write("You have baked so much dough that you warped space-time. (good job)")
        st.write("A portal opens... your future self steps out!")
        st.write("'Listen. You have to restart, or humanity and the universe is doomed.'")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go back in time (prestige)"):
                st.snow()
                st.write("Rewinding time...")
                time.sleep(2)
                st.session_state.pizza_points = 0
                st.session_state.alien_visited = True 
                st.session_state.multiplier = st.session_state.multiplier * 5
                st.session_state.time_travel_visited = True
                st.rerun()
        with col2:
            if st.button("Ignore and Bake More."):
                fate = random.random()
                if fate > 0.5:
                    st.session_state.pizza_points *= 2
                    st.balloons()
                    st.success("YOU BROKE REALITY! SCORE DOUBLED!")
                    st.session_state.time_travel_visited = True
                    st.rerun()
                else:
                    st.error("The universe collapsed...")
                    time.sleep(2)
                    st.session_state.pizza_points = 0
                    st.rerun()
        st.stop()

    # 3. ALIEN INVASION (240,000)
    elif st.session_state.pizza_points >= 240000 and not st.session_state.alien_visited:
        st.toast("Unidentified flying object observed!(⏃⌰⟟⟒⋏ ⌰⍜⎐⟒ ⌿⟟⋉⋉⏃)", icon="🛸")
        st.write("Your pizzas are getting known in outer space.")
        st.write("An alien wants to try your pizza!(⊬⍜, ☌⟟⎐⟒ ⋔⟒ ⌇⍜⋔⟒ ⍜⎎ ⊬⍜⎍⍀ ⌿⟟⋉⋉⏃)")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Feed the Alien"):
                time.sleep(3)
                st.success("IT LOVES IT! +10,000 Points!")
                st.session_state.pizza_points += 10000
                st.session_state.alien_visited = True
                st.rerun()
        with col2:
            if st.button("Decline"):
                st.error("The alien destroys your pizzeria!(⍙⊑⊬ ⎅⟟⎅ ⊬⍜⎍ ⋏⍜⏁ ☌⟟⎐⟒ ⌿⟟⋉⋉⏃)")
                time.sleep(2)
                st.session_state.pizza_points = 0
                st.session_state.alien_visited = True
                st.rerun()
        st.stop()

    # 4. PASS THE RECIPE (60,000 - The "Successor" Event)
    elif st.session_state.pizza_points >= 60000:
        st.write("### 👴 You are getting old!")
        st.write("You're ready to pass on the secret recipe.")
        
        successor = st.selectbox("Who will inherit the shop?", 
             ["Choose...", "John (Friend)", "Bob (Experienced chef)", "Per Per (Stranger)", "Emma (Regular)", "Lars (Son)", "Charles (Doctor)", "Luna (Stranger)"])
        
        if successor != "Choose...":
            if "Stranger" in successor:
                import time
                st.write("Transferring the recipe...")
                time.sleep(2) 
                st.error("What are they doing with those matches?!")
                time.sleep(1)
                st.write('They had no idea how to run a shop. They "accidentally" burned it down! ' + successor + ' enjoyed watching the pizzas crackle to dust.')
                
                if st.button("The pizzeria is gone. Start over?"):
                    st.session_state.pizza_points = 0
                    st.rerun()
            
            elif "Doctor" in successor:
                st.write("Charles: 'You look ill. Take this medicine?'")
                choice = st.radio("Do you take it?", ["Select...", "Yes", "No"])
                if choice == "Yes":
                    st.success("MIRACLE! You feel young again! (-5000 pts)")
                    st.session_state.pizza_points -= 5000
                    if st.button("Back to Kitchen"): st.rerun()
                elif choice == "No":
                    st.error("YOU DIED.")
                    if st.button("Restart"): 
                        st.session_state.pizza_points = 0
                        st.rerun()
            
            elif "Bob" in successor:
                st.session_state.multiplier = 2
                st.success("Bob is a genius! 2x Multiplier Active! ⚡")
                st.session_state.pizza_points = 10000
                if st.button("Bob!"): st.rerun()
            
            else:
                st.success(f"You gave the shop to {successor}. Legacy safe! ❤️")
                if st.button("Retire in Peace"):
                    st.session_state.pizza_points = 0
                    st.rerun()
        st.stop()

    # 5. LOWER RANKS
    elif st.session_state.pizza_points >= 30000:
        st.write("🌎 Your pizzas are world famous!")
    elif st.session_state.pizza_points >= 12000:
        st.write("### 🏆 Rank: MASTER CHEF")
    elif st.session_state.pizza_points >= 5000:
        st.write("### 🥈 Rank: Kitchen Assistant")
    else:
        st.write("### 😂 Rank: NOOB (Everyone makes fun of you, haha)")


# ==========================================
#  SECTION 3: MINI-GAMES
# ==========================================
elif section == "🎮Mini-Games":
    st.title("Mini-Games 🕹️ tihi")
    game_choice = st.radio("Select Game:", ["🔨 Whack-A-Mole", "🔢 Guess a Number"], horizontal=True)
    st.markdown("---")

    # --- WHACK A MOLE ---
if game_choice == "🔨 Whack-A-Mole":
        st.subheader("Whack-A-Mole: Arcade Edition")
        st.write("Hit 🐹 (+50), Hit 💎 (+500), AVOID 💣!")

        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3] * 3
        
        # Start-værdier (hvis de ikke findes)
        if 'mole_pos' not in st.session_state: st.session_state.mole_pos = random.randint(0, 8)
        if 'game_item' not in st.session_state: st.session_state.game_item = "🐹"

        for i in range(9):
            with columns[i]:
                # Er muldvarpen her?
                if i == st.session_state.mole_pos:
                    if st.button(st.session_state.game_item, key=f"mole_{i}"):
                        # 1. TJEK HVAD VI RAMTE
                        if st.session_state.game_item == "🐹":
                            points = 50 * st.session_state.multiplier
                            st.session_state.pizza_points += points
                            st.success(f"HIT! +{points}")
                        elif st.session_state.game_item == "💎":
                            points = 500 * st.session_state.multiplier
                            st.session_state.pizza_points += points
                            st.balloons()
                            st.success(f"JACKPOT! +{points}")
                        elif st.session_state.game_item == "💣":
                            st.session_state.pizza_points = 0
                            st.error("BOOM! Points lost.")
                        
                        # 2. FLYT MULDVARP
                        st.session_state.mole_pos = random.randint(0, 8)
                        
                        # 3. VÆLG NY ITEM (VIGTIGT!)
                        chance = random.random()
                        limit_bomb = 0.80 if st.session_state.luck_charm else 0.90
                        
                        if chance < 0.70: st.session_state.game_item = "🐹"
                        elif chance < limit_bomb: st.session_state.game_item = "💣"
                        else: st.session_state.game_item = "💎"
                        
                        st.rerun()
                
                else:
                    # Tomt hul (Miss)
                    if st.button("🕳️", key=f"hole_{i}"):
                        # 1. FLYT MULDVARP
                        st.session_state.mole_pos = random.randint(0, 8)
                        
                        # 2. VÆLG NY ITEM (HER VAR FEJLEN FØR!)
                        # Nu skifter vi også kostume, selvom man klikker ved siden af!
                        chance = random.random()
                        limit_bomb = 0.80 if st.session_state.luck_charm else 0.90
                        
                        if chance < 0.70: st.session_state.game_item = "🐹"
                        elif chance < limit_bomb: st.session_state.game_item = "💣"
                        else: st.session_state.game_item = "💎"
                        
                        st.rerun()

    # --- GUESS A NUMBER ---
    elif game_choice == "🔢 Guess a Number":
        st.title("Guess a number!")

    # Initialiser session state (Hukommelsen)
        if 'hemmeligt_tal' not in st.session_state:
            st.session_state.hemmeligt_tal = random.randint(1, 100)
            st.session_state.forsøg = 0
            st.session_state.brugernavn = random.choice(["number_guesser", "ooga booga", "python_fan123", "AI超级粉丝", "CoolName", "nooob", "streamlit", "VScode", "User142", "ShuaiGuo"])
            st.session_state.game_over = False

    # Velkomst
        st.write(f"Hello **{st.session_state.brugernavn}**! I am thinking of a number between 1 and 100...")

    # Input felt
        gæt = st.number_input("What do you guess?", min_value=1, max_value=100, step=1)

    # Gæt-knappen
        if st.button("Guess!") and not st.session_state.game_over:
            st.session_state.forsøg += 1
        
            if gæt == st.session_state.hemmeligt_tal:
                st.balloons()
                st.success(f"YAY! You guessed it! With {st.session_state.forsøg} attempt(s)!")
            
            # Præmier
                point = st.session_state.forsøg
                if point == 1:
                    st.write("### OMG!!! 🫏 You got Nothing! Congrats!")
                elif point < 3:
                    st.write("### WOW! 💎 You got Diamond!")
                elif point < 6:
                    st.write("### Nice! 🥇 You got Gold!")
                elif point < 10:
                    st.write("### 🥈 You got Silver!!")
                else:
                    st.write("### 🥉 You got Bronze!")
            
                st.session_state.game_over = True

            elif gæt < st.session_state.hemmeligt_tal:
                st.warning("The number is bigger!")
            else:
                st.warning("The number is smaller!")


# ==========================================
#  SECTION 4: MOOD CHECKER
# ==========================================
elif section == "Mood-Checker":
    st.title("How are you feeling today?")
    mood = st.radio("Choose the mood that suits you!", ["Choose", "Good!^^", "Bad:(", "Both", "Angry"], 
    horizontal=True)

    if mood == "Good!^^":
        st.balloons()
        st.success("Yay! Keep shining!✨" )
    elif mood == "Bad:(":
        st.info("No worries! Have some hot chocolate. ☕")
    elif mood == "Both":
        st.balloons()
        st.write("“Det var godt! Bliv ved med at skinne” idk bruh 😭")

    elif mood == "Angry":
        st.write("### 11 Angry, Fascinating, Funny Quotes ☹️😠")
        
        st.write("""
        * Angry people attract angry people, live in an angry world.😡🌍
        * Angry is heavy. Let it go😒🍃
        * Leave me alone. Go away. I dont care.
        * Anger makes us feel so isolated.
        * Actions louder than words, and my silence arms with.🫨
        * For every minute you are angry you lost sixty seconds of happiness.
        * Let your love be stronger than your anger.❤️‍🩹
        * Angry not always good.
        """)
        st.image("https://i.pinimg.com/originals/cf/db/44/cfdb446d79a7787eb02794645208817f.png", width=1000)

elif section == "🛠️ Tools":
    st.title("🛠️ Productivity Tools")
    tool_choice = st.radio("Choose Tool:", ["📝 To-Do List", "🎲 Decision Maker", "⚖️ BMI calculator"], horizontal=True)
    st.markdown("---")

    # --- TO DO LIST ---
    if tool_choice == "📝 To-Do List":
        st.subheader("My Tasks")
        
        # Input for new task
        col1, col2 = st.columns([3, 1])
        with col1:
            new_task = st.text_input("New Task:", placeholder="E.g., Buy Milk...")
        with col2:
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("Add Task ➕"):
                if new_task:
                    st.session_state.todo_list.append(new_task)
                    st.rerun()
        
        # Display the list
        st.write("### Your List:")
        if not st.session_state.todo_list:
            st.info("You have no tasks! Relax^^")
        else:
            for i, task in enumerate(st.session_state.todo_list):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.write(f"**{i+1}.** {task}")
                with c2:
                    if st.button("Done ✅", key=f"delete_{i}"):
                        st.session_state.todo_list.pop(i)
                        st.rerun()
            
            if st.button("Clear All 🗑️"):
                st.session_state.todo_list = []
                st.rerun()

    elif tool_choice == "🎲 Decision Maker":
        st.subheader("Can't decide?")
        options_input = st.text_area("Enter options (separated by comma):", "Streamlit, Python, VScode")
        if st.button("Decide"):
            options = options_input.split(",")
            choice = random.choice(options)
            st.success(f"I think you should choose: **{choice.strip()}**")
            st.balloons()

    elif tool_choice == "⚖️ BMI calculator":
        st.subheader("BMI calculator")
        st.write("Enter your height and weight to see your BMI.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg):", min_value=1.0, value=65.0, step=0.5)
        
        with col2:
            height = st.number_input("Height (cm):", min_value=50.0, value=170.0, step=1.0)
            
        if st.button("Calculate BMI"):
            # Matematik: Vægt / (Højde i meter * Højde i meter)
            height_m = height / 100
            bmi = round(weight / (height_m ** 2), 2)
            
            st.metric("Your BMI is:", bmi)
            st.success("Remember: Numbers are just numbers! The most important thing is that you feel good and are happy. ❤️")

            st.info("Did you know? Muscle weighs more than fat, so BMI doesn't apply to everyone!^^")
