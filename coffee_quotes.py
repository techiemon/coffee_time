# Coffee quotes and jokes for the Coffee Time Notification System
import random

COFFEE_QUOTES = [
    "May your coffee be strong and your Monday be short.",
    "Today's good mood is sponsored by coffee.",
    "Caffeine - It maintains my sunny personality.",
    "Coffee helps me maintain my 'never killed anyone streak.'",
    "I put coffee in my coffee.",
    "The most dangerous drinking game is seeing how long I can go without coffee.",
    "I like coffee because it gives me the illusion that I might be awake.",
    "Sometimes I go hours without drinking coffee... it's called sleeping.",
    "Life without coffee is like something without something... sorry, I haven't had any coffee yet.",
    "Coffee is the best medicine.",
    "I like my coffee like I like myself: strong, sweet, and too hot for you.",
    "Everyone should believe in something. I believe I will have another coffee.",
    "7 days without coffee makes one WEAK.",
    "Doctors found traces of blood in my coffee stream.",
    "Coffee, because adulting is hard.",
    "Coffee owns me, and I'm fine with that.",
    "You're brew-tiful.",
    "It's coffee o'clock.",
    "I don't have a problem with caffeine. I have a problem without it.",
    "Wanna hear a joke? Decaf.",
    "Maybe she's born with it. Maybe it's caffeine.",
    "Drink coffee and pretend to know what you're doing.",
    "Coffee, the favorite drink of the civilized world.",
    "Without my morning coffee, I'm just like a dried-up piece of goat.",
    "May your coffee kick in before reality does.",
    "Humanity runs on coffee.",
    "I put instant coffee in a microwave oven and almost went back in time.",
    "When life gives you lemons, trade them for coffee.",
    "Life happens, coffee helps.",
    "A bad day with coffee is better than a good day without it.",
    "I don't know how people live without coffee, I really don't.",
    "People say money can't buy happiness. They lie. Money buys coffee, coffee makes me happy!",
    "I orchestrate my mornings to the tune of coffee.",
    "Adventure in life is good... consistency in Coffee even better.",
    "The road to success is paved in coffee.",
    "There is no life without water. Because water is needed to make coffee.",
    "Given enough coffee, I could rule the world.",
    "Coffee is a way of stealing time that should by rights belong to your older self.",
    "Life is too short to drink bad coffee.",
    "Some coffee, plus some thinking, equals some great ideas.",
    "A mathematician is a device for turning coffee into theorems.",
    "Why did the hipster burn his tongue? Because he drank his coffee before it was cool.",
    "Science may never come up with a better office communication system than the coffee break.",
    "Espresso yourself. So many blends, so little time.",
    "Take life one sip at a time, and stay grounded.",
    "Better latte than never.",
    "Coffee: because crack is bad for you.",
    "I like my coffee how I like my mornings: dark and strong.",
    "Procaffeinating: the tendency to not start anything until you've had a cup of coffee.",
    "Coffee is my love language."
]

def get_random_quote():
    """Return a random coffee quote"""
    return random.choice(COFFEE_QUOTES)

def get_quote_count():
    """Return the total number of quotes available"""
    return len(COFFEE_QUOTES)
