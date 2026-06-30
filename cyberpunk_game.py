"""
Cyberpunk Night City text adventure game for Discord.

Trigger with !cyberpunk or !nc to start a session in any channel.
Players respond with choice numbers (1-4) or short text commands.
Type !quit or !nc quit to end a session.
"""

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Story node definitions
# Each node: {"text": str, "choices": [(label, next_node), ...], "on_enter": callable|None}
# ---------------------------------------------------------------------------

def _make_nodes():
    nodes = {}

    # -----------------------------------------------------------------------
    # ACT 1 – The Alley
    # -----------------------------------------------------------------------
    nodes["start"] = {
        "text": (
            "```\n"
            "╔══════════════════════════════════════════╗\n"
            "║   NIGHT CITY  //  CIRCA 2077             ║\n"
            "║   [ A TEXT ADVENTURE ]                   ║\n"
            "╚══════════════════════════════════════════╝\n"
            "```\n"
            "You're strolling through a grimy alley in **Night City**. "
            "Neon signs flicker above, casting the wet pavement in sickly pink and blue. "
            "You've got next to no eddies and a handful of basic implants — nothing to write home about.\n\n"
            "Two **Tyger Claws** step in front of the alley's exit. One wields a katana; "
            "the other levels a Lexington pistol straight at your chest. "
            "They flash gang ink and demand your eddies. Death's on the table if you hesitate.\n\n"
            "At your feet: a **lead pipe**. On the trash can to your right: a **DR-5 Nova** revolver. "
            "Both are just within arm's reach.\n\n"
            "**What do you do?**\n"
            "1. Turn and run back deeper into the alley.\n"
            "2. Grab the lead pipe.\n"
            "3. Snatch the DR-5 Nova off the trash can.\n"
            "4. Hand over your eddies and beg for mercy."
        ),
        "choices": {
            "1": "run_away",
            "2": "grab_pipe",
            "3": "grab_nova",
            "4": "pay_up",
        },
    }

    nodes["run_away"] = {
        "text": (
            "You bolt back into the alley. The Tyger Claws laugh and give chase — "
            "their footsteps echo off dumpsters and chain-link. "
            "You take a hard turn into a side passage, leap a rusted fence, and lose them in the maze of Night City back-streets.\n\n"
            "Heart hammering, you slump against a concrete wall. No loot. No ride. "
            "But you're still breathing — and in Night City, that's a win.\n\n"
            "**You escaped, but left empty-handed. Street Cred: 0.**\n\n"
            "Type `!cyberpunk` to play again."
        ),
        "choices": {},
        "end": True,
    }

    nodes["pay_up"] = {
        "text": (
            "You dig through your pockets and hand over every last eddie. "
            "The Tyger Claw with the pistol snatches it, counts it, and sneers. "
            "\"Broke-ass gonk.\" They saunter off, leaving you crouched in the filth.\n\n"
            "**You survived, but lost everything. Street Cred: -1.**\n\n"
            "Type `!cyberpunk` to play again."
        ),
        "choices": {},
        "end": True,
    }

    nodes["grab_pipe"] = {
        "text": (
            "Your fingers close around the cold steel pipe just as the Tyger Claw with the pistol "
            "tracks it and fires — a warning shot sparks off the wall an inch from your ear.\n\n"
            "\"Next one goes through your skull, gonk.\"\n\n"
            "The pipe's still in your hand. The pistol's pointed at your face. "
            "Your move.\n\n"
            "**What do you do?**\n"
            "1. Throw the pipe at the shooter and charge.\n"
            "2. Drop the pipe and go for the DR-5 Nova instead.\n"
            "3. Use the pipe to deflect and rush the katana wielder.\n"
            "4. Surrender and drop the pipe."
        ),
        "choices": {
            "1": "pipe_throw",
            "2": "pipe_to_nova",
            "3": "pipe_rush_katana",
            "4": "pay_up",
        },
    }

    nodes["pipe_throw"] = {
        "text": (
            "You hurl the pipe at the shooter's gun hand. "
            "It cracks against his wrist — the Lexington skids across the pavement. "
            "You're already sprinting. The katana wielder slashes; you duck under it, drive a shoulder "
            "into his ribs, and slam him into the alley wall.\n\n"
            "The disarmed shooter scrambles for his gun. You get there first, "
            "scoop it up, and train it on both of them. "
            "\"Night's not going the way you planned, choom.\"\n\n"
            "They freeze.\n\n"
            "**What do you do?**\n"
            "1. Order them to strip their gear and leave.\n"
            "2. Knock them both out and take everything.\n"
            "3. Let them walk — this is already enough heat."
        ),
        "choices": {
            "1": "disarm_and_loot",
            "2": "knock_out_loot",
            "3": "let_them_walk_no_loot",
        },
    }

    nodes["pipe_to_nova"] = {
        "text": (
            "You feint a swing with the pipe, buying a split second. "
            "The pipe clatters to the ground as you lunge for the DR-5 Nova.\n\n"
            "→ Go to **Grab Nova** outcome."
        ),
        "choices": {"1": "grab_nova_ambush"},
        "_redirect": "grab_nova",
    }

    nodes["pipe_rush_katana"] = {
        "text": (
            "You swing the pipe at the katana, deflecting the blade with a clang that rattles your teeth. "
            "The swordsman stumbles back. You step inside his guard and clock him across the jaw — "
            "he drops.\n\n"
            "The shooter fires twice; both shots go wide. You rush him, slam the pipe into his forearm, "
            "and wrench the Lexington free. He backs against the wall, hands up.\n\n"
            "**Both Tyger Claws are down or surrendered.**\n\n"
            "**What do you do?**\n"
            "1. Loot them and go.\n"
            "2. Tie them up with their own belts and call the NCPD tip line.\n"
            "3. Leave them — you got enough heat tonight."
        ),
        "choices": {
            "1": "knock_out_loot",
            "2": "call_ncpd",
            "3": "let_them_walk_no_loot",
        },
    }

    nodes["grab_nova"] = {
        "text": (
            "Your hand brushes the cold frame of the DR-5 Nova — and the Tyger Claw "
            "raises his Lexington to your temple. Classic ambush bait.\n\n"
            "\"Smart move, gonk. Now you've got a gun *and* a bullet with your name on it. "
            "Give me everything, or I redecorate this alley.\"\n\n"
            "**What do you do?**\n"
            "1. Comply. It's not worth dying over.\n"
            "2. Call his bluff — spin and fire the Nova in one move.\n"
            "3. Drop low, let him shoot past you, and tackle him."
        ),
        "choices": {
            "1": "pay_up",
            "2": "grab_nova_shoot",
            "3": "nova_tackle",
        },
    }

    nodes["grab_nova_ambush"] = nodes["grab_nova"]

    nodes["grab_nova_shoot"] = {
        "text": (
            "Time compresses. You spin on your heel, bringing the Nova up in a tight arc. "
            "**Bang.** The shot punches through his right shoulder. "
            "He staggers back against the wall, Lexington clattering to the ground, "
            "clutching the wound and hissing through gritted teeth.\n\n"
            "The katana wielder lunges. You sidestep, grab his wrist mid-swing, "
            "and snap his balance. He trips over his fallen friend. "
            "You press the Nova's barrel to the bridge of his nose.\n\n"
            "\"Boo.\"\n\n"
            "His eyes go wide. He freezes.\n\n"
            "**What do you do?**\n"
            "1. Spare him. Tell him to spread the word — Cyber Psycho's in town.\n"
            "2. Knock him out and loot both of them.\n"
            "3. Let them both limp away. You've made your point."
        ),
        "choices": {
            "1": "spare_spread_word",
            "2": "knock_out_loot",
            "3": "let_them_walk_no_loot",
        },
    }

    nodes["nova_tackle"] = {
        "text": (
            "You drop into a roll. His shot sparks off the dumpster behind you. "
            "You come up inside his reach and drive him into the ground hard — "
            "Nova in your hand, his gun arm pinned under your knee.\n\n"
            "The katana wielder hesitates one second too long. "
            "You fan the Nova toward him. \"Don't.\"\n\n"
            "He doesn't.\n\n"
            "**What do you do?**\n"
            "1. Loot them both and disappear.\n"
            "2. Disarm them, take their valuables, let them walk.\n"
            "3. Call the NCPD tip line — anonymously."
        ),
        "choices": {
            "1": "knock_out_loot",
            "2": "disarm_and_loot",
            "3": "call_ncpd",
        },
    }

    # -----------------------------------------------------------------------
    # Resolution nodes
    # -----------------------------------------------------------------------
    nodes["spare_spread_word"] = {
        "text": (
            "\"Run. Tell everyone in the Claws you crossed someone you shouldn't have.\"\n\n"
            "The surviving Tyger Claw scrambles to his feet and bolts. "
            "You hear him yelling around the corner: *\"She's a Cyber Psycho! Took out three of us!\"*\n\n"
            "**+2 Street Cred.**\n\n"
            "You search the downed gangoon. Light haul:\n"
            "• **Lexington pistol** (+1 to ranged combat)\n"
            "• **87 eddies**\n"
            "• A pack of cigarettes (useful for certain NPC conversations)\n\n"
            "You pocket everything and step out of the alley. "
            "Night City's still humming, indifferent as ever.\n\n"
            "**What now?**\n"
            "1. Head to a ripperdoc — check for any wounds and maybe upgrade.\n"
            "2. Get some wheels. You can't keep running jobs on foot.\n"
            "3. Check the metaverse for contracts — you need eddies."
        ),
        "choices": {
            "1": "ripperdoc",
            "2": "get_wheels",
            "3": "metaverse_contracts",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Lexington pistol", "pack of cigarettes"]),
            s.__setitem__("eddies", s["eddies"] + 87),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 2),
        ),
    }

    nodes["knock_out_loot"] = {
        "text": (
            "You work fast. Four Tyger Claws, one alley — you're thorough.\n\n"
            "**Loot acquired:**\n"
            "• **214 eddies**\n"
            "• DR-5 Nova revolver\n"
            "• Lexington pistol\n"
            "• Red jacket with Tyger Claw patch *(+1 Stealth in gang territory)*\n"
            "• Silver ring with red stone *(+1 Charisma)*\n"
            "• 83 rounds of mixed ammo\n"
            "• Two packs of cigarettes\n"
            "• Two cans of Bi-Carb stim\n\n"
            "**+3 Street Cred.**\n\n"
            "The alley's quiet again. Night City doesn't care — it never does.\n\n"
            "**What now?**\n"
            "1. Get some wheels. You've earned it.\n"
            "2. Hit a ripperdoc — check those wounds and maybe upgrade.\n"
            "3. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "ripperdoc",
            "3": "metaverse_contracts",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["DR-5 Nova", "Lexington", "red Tyger Claw jacket",
                                      "silver ring", "2x cigarettes", "2x Bi-Carb"]),
            s.__setitem__("eddies", s["eddies"] + 214),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 3),
        ),
    }

    nodes["disarm_and_loot"] = {
        "text": (
            "You strip their hardware and lift their eddies, leaving them bruised but breathing.\n\n"
            "**Loot acquired:**\n"
            "• **156 eddies**\n"
            "• Lexington pistol\n"
            "• Katana *(+2 melee damage)*\n"
            "• Red jacket with Tyger Claw patch\n\n"
            "**+2 Street Cred.**\n\n"
            "They stumble away into the dark. You've got gear now.\n\n"
            "**What now?**\n"
            "1. Get some wheels.\n"
            "2. Hit a ripperdoc.\n"
            "3. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "ripperdoc",
            "3": "metaverse_contracts",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Lexington", "katana", "red Tyger Claw jacket"]),
            s.__setitem__("eddies", s["eddies"] + 156),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 2),
        ),
    }

    nodes["let_them_walk_no_loot"] = {
        "text": (
            "You wave them off. They go — fast.\n\n"
            "No loot, but no heat either. Sometimes that's the play.\n\n"
            "**+1 Street Cred** for the reputation of showing mercy.\n\n"
            "**What now?**\n"
            "1. Get some wheels.\n"
            "2. Hit a ripperdoc.\n"
            "3. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "ripperdoc",
            "3": "metaverse_contracts",
        },
        "on_enter": lambda s: s.__setitem__("street_cred", s.get("street_cred", 0) + 1),
    }

    nodes["call_ncpd"] = {
        "text": (
            "You dial the anonymous NCPD tip line and drop a pin. "
            "Two black-and-whites roll up within minutes — Night City's Finest "
            "are surprisingly fast when it's not your emergency.\n\n"
            "You watch from a rooftop as they bag the Claws. "
            "Probably out by morning, but that's not your problem.\n\n"
            "**+1 Street Cred** (civic duty, surprisingly).\n\n"
            "**What now?**\n"
            "1. Get some wheels.\n"
            "2. Hit a ripperdoc.\n"
            "3. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "ripperdoc",
            "3": "metaverse_contracts",
        },
        "on_enter": lambda s: s.__setitem__("street_cred", s.get("street_cred", 0) + 1),
    }

    # -----------------------------------------------------------------------
    # ACT 2 – City Choices
    # -----------------------------------------------------------------------
    nodes["ripperdoc"] = {
        "text": (
            "Doc Ryder's place is a converted storage unit in Kabuki, "
            "walls lined with chrome arms and optical rigs floating in amber fluid.\n\n"
            "\"Sit,\" she says, already scanning you. \"Nothing fatal. "
            "Few cracked ribs, one gash that needs staples.\"\n\n"
            "She patches you up for **50 eddies** and offers upgrades:\n"
            "• **Kerenzikov reflex booster** — 600 eddies *(+2 to combat dodge)*\n"
            "• **Subdermal armor** — 450 eddies *(+2 to damage resistance)*\n"
            "• **Skip the upgrades** — save your eddies.\n\n"
            "**What do you choose?**\n"
            "1. Kerenzikov reflex booster (600 eddies).\n"
            "2. Subdermal armor (450 eddies).\n"
            "3. Just the patch-up. Get out."
        ),
        "choices": {
            "1": "buy_kerenzikov",
            "2": "buy_subdermal",
            "3": "leave_ripperdoc",
        },
    }

    nodes["buy_kerenzikov"] = {
        "text": (
            "Doc Ryder installs the Kerenzikov in under an hour. "
            "When you stand up, the world feels a half-second slower — "
            "in the best possible way.\n\n"
            "**Kerenzikov installed. +2 combat dodge. -650 eddies.**\n\n"
            "**What now?**\n"
            "1. Get some wheels.\n"
            "2. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "metaverse_contracts",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Kerenzikov reflex booster"]),
            s.__setitem__("eddies", s["eddies"] - 650),
        ),
    }

    nodes["buy_subdermal"] = {
        "text": (
            "The subdermal mesh goes in layer by layer. "
            "You leave the ripperdoc feeling like you're wearing invisible body armor — "
            "because you are.\n\n"
            "**Subdermal armor installed. +2 damage resistance. -500 eddies.**\n\n"
            "**What now?**\n"
            "1. Get some wheels.\n"
            "2. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "metaverse_contracts",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Subdermal armor"]),
            s.__setitem__("eddies", s["eddies"] - 500),
        ),
    }

    nodes["leave_ripperdoc"] = {
        "text": (
            "\"Come back when you've got real money,\" Doc Ryder calls after you.\n\n"
            "**-50 eddies (patch-up).**\n\n"
            "**What now?**\n"
            "1. Get some wheels.\n"
            "2. Check the metaverse for contracts."
        ),
        "choices": {
            "1": "get_wheels",
            "2": "metaverse_contracts",
        },
        "on_enter": lambda s: s.__setitem__("eddies", s["eddies"] - 50),
    }

    nodes["get_wheels"] = {
        "text": (
            "A vehicle dealer on Broad Street has a decent compact lot. "
            "You've got enough eddies to make something happen.\n\n"
            "**Available compact rides:**\n"
            "1. **Quartz \"Little Beast\"** — 3,000 ED\n"
            "   Hybrid, sleek silver body, neon trim. Fuel-efficient, blends into traffic.\n"
            "2. **Makigai MaiMai P120** — 8,000 ED\n"
            "   Full electric, whisper-quiet, wide customization. Tiny footprint. Ideal for the city.\n"
            "3. **Villefort Corrigidor** — 5,500 ED\n"
            "   Rugged compact pickup. Handles Badlands terrain, takes a beating.\n"
            "4. **Skip it** — you don't need wheels right now."
        ),
        "choices": {
            "1": "buy_little_beast",
            "2": "buy_maimai",
            "3": "buy_corrigidor",
            "4": "metaverse_contracts",
        },
    }

    nodes["buy_little_beast"] = {
        "text": (
            "You hand over 3,000 eddies and drive off in the Little Beast. "
            "The hybrid engine purrs almost silently. Neon trim pulses as you ease into traffic — "
            "nobody gives you a second look.\n\n"
            "**Quartz Little Beast acquired. -3,000 eddies.**\n\n"
            "**What now?**\n"
            "1. Check the metaverse for contracts.\n"
            "2. Explore Night City — see what the night offers."
        ),
        "choices": {
            "1": "metaverse_contracts",
            "2": "explore_city",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Quartz Little Beast"]),
            s.__setitem__("eddies", s["eddies"] - 3000),
        ),
    }

    nodes["buy_maimai"] = {
        "text": (
            "8,000 eddies — your entire haul, near enough. "
            "But when you slide into the MaiMai P120, the touch-screen dashboard "
            "lights up cyan and the electric motor kicks in like silk.\n\n"
            "Compact. Silent. The perfect shadow for Night City streets.\n\n"
            "**Makigai MaiMai P120 acquired. -8,000 eddies.**\n\n"
            "**What now?**\n"
            "1. Check the metaverse for contracts.\n"
            "2. Cruise the city — clear your head."
        ),
        "choices": {
            "1": "metaverse_contracts",
            "2": "explore_city",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Makigai MaiMai P120"]),
            s.__setitem__("eddies", s["eddies"] - 8000),
        ),
    }

    nodes["buy_corrigidor"] = {
        "text": (
            "The Corrigidor's dented but solid — the kind of vehicle "
            "that looks like it's already been in a fight and won. "
            "5,500 eddies and the dealer barely haggled.\n\n"
            "Built for the Badlands. If that's where the work is, this is the right call.\n\n"
            "**Villefort Corrigidor acquired. -5,500 eddies.**\n\n"
            "**What now?**\n"
            "1. Check the metaverse for contracts.\n"
            "2. Cruise the Badlands perimeter — get the lay of the land."
        ),
        "choices": {
            "1": "metaverse_contracts",
            "2": "explore_badlands_perimeter",
        },
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["Villefort Corrigidor"]),
            s.__setitem__("eddies", s["eddies"] - 5500),
        ),
    }

    nodes["explore_city"] = {
        "text": (
            "You cruise Watson, Japantown, Heywood — the city breathing around you. "
            "Neon bleeds into rain-slick streets. A street performer plays shamisen "
            "outside a noodle stand. Someone's getting chased two blocks over; "
            "not your problem.\n\n"
            "An hour in, your neural link pings — a fixer named **Rook** wants a meet. "
            "Says she's got something quiet and profitable.\n\n"
            "**What do you do?**\n"
            "1. Take the meet.\n"
            "2. Ignore it and check the metaverse for contracts yourself.\n"
            "3. Head home and call it a night."
        ),
        "choices": {
            "1": "fixer_meet",
            "2": "metaverse_contracts",
            "3": "end_night",
        },
    }

    nodes["explore_badlands_perimeter"] = {
        "text": (
            "The Badlands open up east of the city like a wound in the earth. "
            "Flat, dark, and lethal. You drive the perimeter, clocking sight-lines, "
            "noting broken fence sections and abandoned fuel stations.\n\n"
            "Your neural link pings — a fixer named **Rook** wants a meet. "
            "She heard through the grapevine you know how to handle yourself.\n\n"
            "**What do you do?**\n"
            "1. Take the meet.\n"
            "2. Ignore it and check the metaverse for contracts yourself.\n"
            "3. Head home and call it a night."
        ),
        "choices": {
            "1": "fixer_meet",
            "2": "metaverse_contracts",
            "3": "end_night",
        },
    }

    # -----------------------------------------------------------------------
    # ACT 3 – Contracts
    # -----------------------------------------------------------------------
    nodes["metaverse_contracts"] = {
        "text": (
            "You jack into the metaverse through your neural link. "
            "Contract listings scroll past — corporate gigs, gang bounties, deliveries.\n\n"
            "Tonight's available jobs:\n"
            "1. **Infiltrate a Arasaka facility** — steal a prototype chip. High risk, high reward.\n"
            "2. **Neutralize a Tyger Claw lieutenant** before he can testify to Militech. "
            "Clean, surgical — or not.\n"
            "3. **Deliver goods to the Badlands** — straightforward run, decent pay. "
            "Good excuse to test your wheels.\n"
            "4. **Investigate a suspected Cyber Psycho** — someone's ripping through "
            "Westbrook and NCPD wants answers."
        ),
        "choices": {
            "1": "contract_arasaka",
            "2": "contract_tc_lieutenant",
            "3": "contract_badlands_delivery",
            "4": "contract_cyberpsycho",
        },
    }

    nodes["fixer_meet"] = {
        "text": (
            "Rook meets you at a dim sum joint in Japantown — corner booth, back to the wall. "
            "She's wired: optical implants cycling amber, chrome hand resting on the table.\n\n"
            "\"Heard about the Claws in the alley. Sloppy on their part, clean on yours.\" "
            "She pushes a data chip across the table. \"Got a gig. "
            "Three jobs on offer — pick one, do it right, I'll make sure "
            "the right people hear your name.\"\n\n"
            "**Rook's contracts:**\n"
            "1. **Arasaka facility** — steal a prototype chip. She has the schematics.\n"
            "2. **Badlands delivery** — move sensitive cargo, no questions.\n"
            "3. **Cyber Psycho investigation** — find whoever's painting Westbrook red."
        ),
        "choices": {
            "1": "contract_arasaka",
            "2": "contract_badlands_delivery",
            "3": "contract_cyberpsycho",
        },
    }

    # -----------------------------------------------------------------------
    # CONTRACT: Badlands Delivery
    # -----------------------------------------------------------------------
    nodes["contract_badlands_delivery"] = {
        "text": (
            "The package is already in your trunk — sealed, heavy, and none of your business. "
            "Delivery point: a small settlement in the northeastern Badlands, "
            "45 minutes east. Hand it to a fixer named **Sable**.\n\n"
            "**Pay: 2,400 eddies on delivery.**\n\n"
            "You pull onto the highway heading east. Night City's skyline shrinks behind you. "
            "The Badlands open up — flat, dark, endless.\n\n"
            "Your night-vision kicks on. Hip-hop thumps from the speakers. "
            "You're three minutes out when your scanner flags movement — "
            "two vehicles running dark, parallel to your route.\n\n"
            "**What do you do?**\n"
            "1. Kill the headlights and speed up — lose them.\n"
            "2. Pull off-road and hide the vehicle. Approach the settlement on foot.\n"
            "3. Stop and confront them. It might be other fixers, not hostiles.\n"
            "4. Keep driving and call Sable to warn her."
        ),
        "choices": {
            "1": "badlands_speed",
            "2": "badlands_on_foot",
            "3": "badlands_confront",
            "4": "badlands_call_sable",
        },
    }

    nodes["badlands_speed"] = {
        "text": (
            "You kill the lights and floor it. "
            "The electric motor goes near-silent at speed — "
            "you're a ghost on the Badlands flats.\n\n"
            "The dark vehicles veer to intercept but you're already through the gap. "
            "A shot pings off your bumper — small arms, nothing structural.\n\n"
            "You blow past the settlement entrance and brake hard, "
            "kicking up a rooster tail of dust. Sable's waiting by a fire barrel.\n\n"
            "\"Saw the chase. Nice driving.\" She takes the package.\n\n"
            "**Delivery complete. +2,400 eddies. +1 Street Cred.**\n\n"
            "**What now?**\n"
            "1. Head back to Night City.\n"
            "2. Ask Sable if she's got more work."
        ),
        "choices": {
            "1": "end_night_success",
            "2": "sable_more_work",
        },
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 2400),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 1),
        ),
    }

    nodes["badlands_on_foot"] = {
        "text": (
            "You pull the vehicle into a ravine behind a ridge of scrub rock "
            "and kill the engine. Package on your back, you move toward the settlement "
            "on foot — quarter mile through open terrain, using every shadow.\n\n"
            "The two dark vehicles roll slowly past your hidden car and continue east. "
            "Not looking for a parked target — they were tracking movement.\n\n"
            "Smart call.\n\n"
            "Sable meets you at the perimeter fence. "
            "\"Thought you weren't coming. This way.\" She takes the package, "
            "counts out the eddies from a roll in her jacket.\n\n"
            "**Delivery complete. +2,400 eddies. +2 Street Cred.**\n\n"
            "**What now?**\n"
            "1. Retrieve your vehicle and head back to Night City.\n"
            "2. Ask Sable if she's got more work."
        ),
        "choices": {
            "1": "end_night_success",
            "2": "sable_more_work",
        },
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 2400),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 2),
        ),
    }

    nodes["badlands_confront"] = {
        "text": (
            "You pull over and roll down the window. "
            "One of the dark vehicles slows — then accelerates straight at you.\n\n"
            "Ambush. They knew about the package.\n\n"
            "You punch it. A running firefight breaks out across the Badlands flats — "
            "shots sparking off your chassis, you returning fire through the window.\n\n"
            "One pursuer spins out. The second clips your rear and sends you into a slide — "
            "you recover, drive the bumper into his door, and put him in the ditch.\n\n"
            "You reach the settlement battered but intact. Sable raises an eyebrow at the damage.\n\n"
            "**Delivery complete. +2,400 eddies. Vehicle damaged. +1 Street Cred.**\n\n"
            "**What now?**\n"
            "1. Head back to Night City — get the vehicle fixed.\n"
            "2. Ask Sable who those people were."
        ),
        "choices": {
            "1": "end_night_success",
            "2": "sable_who_were_they",
        },
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 2400),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 1),
        ),
    }

    nodes["badlands_call_sable"] = {
        "text": (
            "\"Two vehicles running dark. They know about the cargo.\"\n\n"
            "Sable doesn't miss a beat. \"Change of route. "
            "There's a dry creek bed two klicks north. Follow it in.\"\n\n"
            "You reroute. The creek bed swallows your vehicle — "
            "the dark runners never spot you. "
            "You emerge behind the settlement and Sable's already waiting.\n\n"
            "\"Good instincts. I like that in a courier.\"\n\n"
            "**Delivery complete. +2,400 eddies. +2 Street Cred.**\n\n"
            "**What now?**\n"
            "1. Head back to Night City.\n"
            "2. Ask Sable if she's got more work."
        ),
        "choices": {
            "1": "end_night_success",
            "2": "sable_more_work",
        },
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 2400),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 2),
        ),
    }

    nodes["sable_more_work"] = {
        "text": (
            "Sable pours two fingers of synthetic whiskey and leans back. "
            "\"You handled that cleaner than most. "
            "I've got a harder job — but it pays triple. "
            "Arasaka has a data vault relay station 10 klicks northeast. "
            "I need what's inside. You in?\"\n\n"
            "**What do you do?**\n"
            "1. Accept the Arasaka job.\n"
            "2. Decline — you've earned enough for tonight.\n"
            "3. Counter-offer: double her triple."
        ),
        "choices": {
            "1": "contract_arasaka",
            "2": "end_night_success",
            "3": "counter_offer_sable",
        },
    }

    nodes["sable_who_were_they"] = {
        "text": (
            "Sable's expression darkens. \"Militech runners. "
            "They've been tracking my shipments for two weeks. "
            "You just made their list.\"\n\n"
            "She refills your glass. \"Which means I owe you one. "
            "I've got a job that could help both of us — "
            "takes Militech off my back and pays you well.\"\n\n"
            "**What do you do?**\n"
            "1. Hear her out.\n"
            "2. Pass — Militech heat is above your pay grade right now.\n"
            "3. Ask for details before committing."
        ),
        "choices": {
            "1": "sable_more_work",
            "2": "end_night_success",
            "3": "sable_more_work",
        },
    }

    nodes["counter_offer_sable"] = {
        "text": (
            "Sable stares at you for a long moment. "
            "Then she laughs — a short, genuine sound that doesn't match her chrome hand.\n\n"
            "\"I like you. Done. But you'd better bring me back clean intel, not excuses.\"\n\n"
            "**Triple + counter accepted. Arasaka job incoming.**"
        ),
        "choices": {"1": "contract_arasaka"},
    }

    # -----------------------------------------------------------------------
    # CONTRACT: Arasaka
    # -----------------------------------------------------------------------
    nodes["contract_arasaka"] = {
        "text": (
            "The Arasaka relay station sits inside a compound in the northern Badlands — "
            "or Watson Industrial, depending on the source. "
            "Two guards visible on the perimeter. Internal layout unknown.\n\n"
            "**Pay: 7,200 eddies on delivery of the prototype chip.**\n\n"
            "You scope the facility from 200 meters with a long-range optic.\n\n"
            "**What's your approach?**\n"
            "1. **Stealth** — cut the fence, avoid guards, in and out silent.\n"
            "2. **Netrun** — hack the door locks and cameras remotely, then walk in.\n"
            "3. **Loud** — breach the front gate and fight your way to the vault.\n"
            "4. **Social engineering** — fake a maintenance uniform and bluff your way past."
        ),
        "choices": {
            "1": "arasaka_stealth",
            "2": "arasaka_netrun",
            "3": "arasaka_loud",
            "4": "arasaka_social",
        },
    }

    nodes["arasaka_stealth"] = {
        "text": (
            "Wire cutters through the fence at a camera blind-spot. "
            "You're inside in ninety seconds, moving low between shadows.\n\n"
            "Two guards on patrol. You time their rotation, "
            "slip between their paths, and reach the relay building. "
            "Locked door — you crack the panel with a basic bypass chip.\n\n"
            "Inside: server racks, a single tech at a terminal, headphones on. "
            "You find the prototype chip in a shielded case on the back shelf. "
            "You're back through the fence before the guard rotation completes.\n\n"
            "**Mission complete. No casualties. +7,200 eddies. +3 Street Cred.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["prototype chip"]),
            s.__setitem__("eddies", s["eddies"] + 7200),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 3),
        ),
    }

    nodes["arasaka_netrun"] = {
        "text": (
            "You jack in from the vehicle 50 meters out. "
            "The facility's ICE is corporate-grade — "
            "layered black walls of intrusion countermeasures. "
            "You hit it with a Breach Protocol sequence, peel back the firewall, "
            "kill the cameras, and unlock the vault door.\n\n"
            "You walk in like you own the place. One guard gives you a long look. "
            "You give him a maintenance worker's nod. He moves on.\n\n"
            "Chip acquired. You're back in your vehicle before the cameras reboot.\n\n"
            "**Mission complete. Ghost run. +7,200 eddies. +4 Street Cred.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["prototype chip"]),
            s.__setitem__("eddies", s["eddies"] + 7200),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 4),
        ),
    }

    nodes["arasaka_loud"] = {
        "text": (
            "You ram the gate and the alarm goes off before you're out of the vehicle. "
            "Six guards respond. You use the MaiMai as cover, picking targets methodically.\n\n"
            "Three down. Two flank from the east. You take a graze across the ribs — "
            "nothing fatal — and put both down. The sixth drops his weapon and runs.\n\n"
            "The vault door requires a physical keycard; you find it on the guard captain. "
            "Chip in hand, you fight your way back to the vehicle through arriving reinforcements "
            "and punch through a closing gate with thirty seconds to spare.\n\n"
            "**Mission complete — loud. +7,200 eddies. +1 Street Cred. -20 health. Vehicle damaged.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["prototype chip"]),
            s.__setitem__("eddies", s["eddies"] + 7200),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 1),
            s.__setitem__("health", s.get("health", 100) - 20),
        ),
    }

    nodes["arasaka_social"] = {
        "text": (
            "You find a maintenance coverall in a dumpster outside the compound — "
            "previous contractor's, still has an ID badge. Close enough.\n\n"
            "The guard at the gate looks at the badge, looks at you. "
            "\"What's the issue today?\"\n\n"
            "\"Cooling unit in rack three. Work order came through an hour ago.\"\n\n"
            "He waves you through. The tech inside doesn't give you a second glance.\n\n"
            "You find the chip, pocket it, and sign out. "
            "\"All fixed,\" you tell the gate guard on the way out. He nods.\n\n"
            "**Mission complete — clean. +7,200 eddies. +5 Street Cred.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s["inventory"].__iadd__(["prototype chip"]),
            s.__setitem__("eddies", s["eddies"] + 7200),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 5),
        ),
    }

    # -----------------------------------------------------------------------
    # CONTRACT: Tyger Claw Lieutenant
    # -----------------------------------------------------------------------
    nodes["contract_tc_lieutenant"] = {
        "text": (
            "**Target:** Kuro Matsuda, Tyger Claw lieutenant. "
            "He's set to testify to Militech investigators tomorrow morning. "
            "Militech wants him silenced — permanently. "
            "The Claws want him silenced too, for different reasons.\n\n"
            "**Pay: 5,500 eddies.**\n\n"
            "He's holed up in a Japantown apartment with two bodyguards. "
            "You've got until 0600.\n\n"
            "**What's your approach?**\n"
            "1. **Eliminate him** — contract as written.\n"
            "2. **Flip him** — warn Matsuda and sell that information to a third party.\n"
            "3. **Burn the contract** — some jobs aren't worth the karma."
        ),
        "choices": {
            "1": "tc_eliminate",
            "2": "tc_flip",
            "3": "tc_refuse",
        },
    }

    nodes["tc_eliminate"] = {
        "text": (
            "0200. Japantown's quiet enough that your footsteps sound loud.\n\n"
            "You go in through the rooftop access — "
            "bodyguards are watching the stairs, not the skylight. "
            "Matsuda's asleep on a cot in the back room.\n\n"
            "You complete the contract. Clean. Professional. "
            "The testimonies die with him.\n\n"
            "**Contract complete. +5,500 eddies. +2 Street Cred.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 5500),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 2),
        ),
    }

    nodes["tc_flip"] = {
        "text": (
            "You slip into Matsuda's apartment, wake him with a hand over his mouth.\n\n"
            "\"I'm the only reason you're alive right now. "
            "Militech put a contract on you. So did the Claws.\"\n\n"
            "He stares at you. Processing. \"What do you want?\"\n\n"
            "\"Everything you were going to tell Militech. "
            "Then you disappear — new face, new city. I'll make sure your testimony "
            "lands somewhere that actually costs Militech more than it costs you.\"\n\n"
            "He talks for an hour. You have enough to shake a mid-level Militech executive "
            "out of his chair — and you sell it to a Night City independent journalist "
            "for 4,000 eddies. Matsuda boards a night transport to Pacifica.\n\n"
            "**Contract burned — but better outcome. +4,000 eddies. +5 Street Cred.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 4000),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 5),
        ),
    }

    nodes["tc_refuse"] = {
        "text": (
            "You send one message back through the metaverse: *Pass.*\n\n"
            "Some jobs aren't worth the eddies. "
            "Whatever Matsuda knows, whatever Militech buries — "
            "that's not the hill you choose.\n\n"
            "You catch a few hours of sleep. In the morning the news feeds report "
            "Matsuda turned himself in to an independent arbiter. "
            "Sometimes things resolve themselves.\n\n"
            "**Contract refused. No payout. +3 Street Cred (reputation for principles).**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: s.__setitem__("street_cred", s.get("street_cred", 0) + 3),
    }

    # -----------------------------------------------------------------------
    # CONTRACT: Cyber Psycho
    # -----------------------------------------------------------------------
    nodes["contract_cyberpsycho"] = {
        "text": (
            "Three incidents in Westbrook in six days. "
            "One corpo security team. Two gang members. One civilian. "
            "No witnesses — just the aftermath, chrome and blood.\n\n"
            "NCPD's file is thin. They think it's Cyber Psychosis: "
            "too much chrome, not enough humanity left to hold it together.\n\n"
            "**Pay: 4,800 eddies (NCPD bounty) + whatever you learn.**\n\n"
            "You start at the most recent scene — a parking structure in Charter Hill.\n\n"
            "**What do you do first?**\n"
            "1. Scan the scene for physical evidence.\n"
            "2. Talk to the neighborhood — someone always sees something.\n"
            "3. Pull the security camera feeds — if any survived."
        ),
        "choices": {
            "1": "psycho_scan",
            "2": "psycho_talk",
            "3": "psycho_cameras",
        },
    }

    nodes["psycho_scan"] = {
        "text": (
            "Your scanner picks up a pattern in the damage — "
            "all attacks targeted chrome first, skin second. "
            "Whoever this is, they're not random. They're hunting *implants*.\n\n"
            "There's a faint chemical signature on the walls: Dorsivex-9, "
            "a black-market inhibitor used when someone's trying to *suppress* Cyber Psychosis, "
            "not trigger it.\n\n"
            "This isn't someone who snapped. This is someone fighting to stay sane "
            "while targeting people for a reason.\n\n"
            "**New lead. What next?**\n"
            "1. Follow the Dorsivex-9 trail — who sells it black market in Westbrook?\n"
            "2. Cross-reference the victims — what did they have in common?\n"
            "3. Set yourself as bait — you've got plenty of chrome."
        ),
        "choices": {
            "1": "psycho_dorsivex",
            "2": "psycho_victims",
            "3": "psycho_bait",
        },
    }

    nodes["psycho_talk"] = nodes["psycho_scan"]
    nodes["psycho_cameras"] = nodes["psycho_scan"]

    nodes["psycho_victims"] = {
        "text": (
            "All three victims worked for **Biotechnica** — a biotech corp "
            "specializing in neural implant research. "
            "Two were researchers. One was a security contractor who worked "
            "their Night City facility.\n\n"
            "You dig deeper. Six months ago, a Biotechnica clinical trial went wrong — "
            "seventeen participants suffered catastrophic Cyber Psychosis. "
            "The company buried it. The researcher running the trial: "
            "**Dr. Mara Sek**, whose file shows her as *deceased* — "
            "accident, six months ago, same week as the trial.\n\n"
            "She's not dead. She's the Cyber Psycho.\n\n"
            "And she's coming for the people who signed off on covering it up.\n\n"
            "**What do you do?**\n"
            "1. Track her down and bring her in alive for the NCPD bounty.\n"
            "2. Find Sek and offer to help her expose Biotechnica instead.\n"
            "3. Sell the intel to Biotechnica — they'll pay to protect their people."
        ),
        "choices": {
            "1": "psycho_capture",
            "2": "psycho_ally",
            "3": "psycho_sell_biotech",
        },
    }

    nodes["psycho_dorsivex"] = nodes["psycho_victims"]
    nodes["psycho_bait"] = nodes["psycho_victims"]

    nodes["psycho_capture"] = {
        "text": (
            "You find Sek in a maintenance tunnel beneath Charter Hill — "
            "shaking, Dorsivex patches covering both arms, "
            "a wall of handwritten notes mapping every Biotechnica executive.\n\n"
            "She fights. Hard. You take a hit that cracks two more ribs, "
            "but you're faster. Non-lethal takedown, cuffs, NCPD transfer.\n\n"
            "She's screaming about the trial as they load her into the cruiser. "
            "The feeds pick it up. By morning it's trending.\n\n"
            "**Bounty collected. +4,800 eddies. +2 Street Cred. "
            "Biotechnica trial story breaks in the news.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 4800),
            s.__setitem__("street_cred", s.get("street_cred", 0) + 2),
        ),
    }

    nodes["psycho_ally"] = {
        "text": (
            "You sit across from Mara Sek in the tunnel, hands visible, "
            "and tell her what you found. She stares at you — chrome eyes "
            "cycling through distrust, hope, desperation.\n\n"
            "\"You'd help me?\"\n\n"
            "\"I'd help you do this *right*. Not like this.\"\n\n"
            "Two days later, with your help compiling the evidence, "
            "Sek's full report on the Biotechnica trial lands in the hands "
            "of three independent journalists simultaneously. "
            "The corp can't suppress it fast enough.\n\n"
            "Sek turns herself in voluntarily. Her trial becomes public. "
            "Biotechnica loses 40% market value in a week.\n\n"
            "**No bounty — but Night City remembers. +8 Street Cred.**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: s.__setitem__("street_cred", s.get("street_cred", 0) + 8),
    }

    nodes["psycho_sell_biotech"] = {
        "text": (
            "Biotechnica's Night City liaison meets you in a parking garage "
            "and doesn't ask questions — just confirms the package is complete "
            "and transfers 12,000 eddies.\n\n"
            "By the next morning, Sek disappears from all records. "
            "The trial story never breaks. You don't ask where she went.\n\n"
            "**+12,000 eddies. -5 Street Cred (word gets around).**\n\n"
            "Type `!cyberpunk` to play again or `!nc status` to see your stats."
        ),
        "choices": {},
        "end": True,
        "on_enter": lambda s: (
            s.__setitem__("eddies", s["eddies"] + 12000),
            s.__setitem__("street_cred", s.get("street_cred", 0) - 5),
        ),
    }

    # -----------------------------------------------------------------------
    # Misc endings
    # -----------------------------------------------------------------------
    nodes["end_night"] = {
        "text": (
            "You park the vehicle, take the stairs to your apartment, "
            "and drop onto the cot still wearing your gear.\n\n"
            "Night City never sleeps — but tonight, you do.\n\n"
            "**Session ended. Type `!cyberpunk` to play again.**"
        ),
        "choices": {},
        "end": True,
    }

    nodes["end_night_success"] = {
        "text": (
            "You point the vehicle back toward Night City. "
            "The skyline rises ahead — neon and steel and a million lives "
            "going sideways at once.\n\n"
            "Tonight was a good night. Those don't happen often here.\n\n"
            "**Session complete. Type `!nc status` to see your final stats, "
            "or `!cyberpunk` to play again.**"
        ),
        "choices": {},
        "end": True,
    }

    return nodes


STORY_NODES = _make_nodes()

HELP_TEXT = (
    "```\n"
    "NIGHT CITY TEXT ADVENTURE\n"
    "─────────────────────────\n"
    "!cyberpunk / !nc   — start a new game\n"
    "!nc status         — show current stats & inventory\n"
    "!nc quit           — end your current session\n"
    "1 / 2 / 3 / 4      — choose an option during a scene\n"
    "```"
)


class GameSession:
    """Active game state for one Discord channel."""

    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.current_node = "start"
        self.inventory: list[str] = []
        self.eddies: int = 0
        self.street_cred: int = 0
        self.health: int = 100


class CyberpunkAdventure:
    """Manages per-channel Cyberpunk text adventure sessions."""

    def __init__(self):
        self._sessions: dict[int, GameSession] = {}

    def has_session(self, channel_id: int) -> bool:
        """Return True if the channel has an active game session."""
        return channel_id in self._sessions

    def start_game(self, channel_id: int) -> str:
        """Start or restart a game session and return the opening scene text."""
        session = GameSession(channel_id)
        self._sessions[channel_id] = session
        return self._render_node(session)

    def quit_game(self, channel_id: int) -> str:
        """End the session and return a confirmation message."""
        self._sessions.pop(channel_id, None)
        return "Session ended. Stay preem, choom. Type `!cyberpunk` to play again."

    def status(self, channel_id: int) -> str:
        """Return a formatted status/inventory string for the active session."""
        session = self._sessions.get(channel_id)
        if not session:
            return "No active session. Type `!cyberpunk` to start."
        inv = ", ".join(session.inventory) if session.inventory else "nothing"
        return (
            f"```\n"
            f"NIGHT CITY STATUS\n"
            f"─────────────────\n"
            f"Health       : {session.health}/100\n"
            f"Eddies       : {session.eddies:,} ED\n"
            f"Street Cred  : {session.street_cred}\n"
            f"Inventory    : {inv}\n"
            f"```"
        )

    def process_input(self, channel_id: int, text: str) -> str | None:
        """
        Process a player's choice and advance the story.
        Returns the next scene text, or None if no session is active.
        """
        session = self._sessions.get(channel_id)
        if not session:
            return None

        node = STORY_NODES.get(session.current_node)
        if not node:
            logger.error("Missing story node: %s", session.current_node)
            self._sessions.pop(channel_id, None)
            return "Relic error: unknown node. Session reset. Type `!cyberpunk` to restart."

        choice = text.strip()
        choices = node.get("choices", {})

        if not choices:
            return None

        if choice not in choices:
            keys = ", ".join(f"`{k}`" for k in choices)
            return f"Night City doesn't know what you mean. Choose: {keys}"

        next_node_key = choices[choice]
        next_node = STORY_NODES.get(next_node_key)
        if not next_node:
            logger.error("Missing next node: %s", next_node_key)
            return "Relic glitch — that path is corrupted. Choose another option."

        # Handle optional redirect (alias nodes)
        if "_redirect" in next_node:
            next_node_key = next_node["_redirect"]
            next_node = STORY_NODES[next_node_key]

        # Run on_enter side-effects (inventory, stats mutations)
        on_enter = next_node.get("on_enter")
        if on_enter:
            try:
                on_enter(session.__dict__)
            except Exception:
                logger.exception("on_enter failed for node %s", next_node_key)

        session.current_node = next_node_key

        if next_node.get("end"):
            self._sessions.pop(channel_id, None)

        return self._render_node_raw(next_node)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _render_node(self, session: GameSession) -> str:
        node = STORY_NODES.get(session.current_node, {})
        return node.get("text", "ERROR: missing scene text.")

    @staticmethod
    def _render_node_raw(node: dict) -> str:
        return node.get("text", "ERROR: missing scene text.")
