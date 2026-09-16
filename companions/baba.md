# Baba — Bat Familiar

Baba is Layn's bat familiar summoned through the **Nightecho Stone**.

## Nightecho Stone

**Wondrous item, rare**  
**Requires attunement by a Rogue with the Soulknife subclass.**

### Living Stone

As a **Bonus Action**, Layn can shape the stone into a bracelet, necklace, ring, amulet, other simple ornament, or back into a plain pebble. It keeps whatever form is chosen.

While worn or held, Layn can hear its faint psionic clicking, a sound only Layn perceives.

### Call of the Roost

As an **Action**, Layn can cast **Find Familiar** from the stone without needing material components, and the casting time is **Action**.

The familiar summoned this way always takes the form of a **bat**.

Once this property is used, it cannot be used again until the **next dawn**.

### Echolocation

While Baba is within **10 feet of Layn**, Layn has **Blindsight out to 10 feet**.

### Mind's Fang

If Baba is within **5 feet of Layn's target**, Layn deals an extra **1d4 psychic damage** to that target when Layn hits it with an attack.

This is an additional damage instance/effect and must be tracked separately from weapon damage, ability modifier damage, and Sneak Attack.

### Echoing Strike

While Baba is within **100 feet of Layn**, when Layn deals **Sneak Attack damage**, Layn can regain **one expended Psionic Energy die**.

Once this property is used, it cannot be used again until Layn finishes a **Long Rest**.

## Baba combat state

The simulator should always track:

- Whether Baba is currently summoned/active.
- Baba's current position.
- Baba's distance from Layn.
- Baba's distance from every relevant target.
- Whether Baba is within 10 ft of Layn for Echolocation.
- Whether Baba is within 5 ft of the attack target for Mind's Fang.
- Whether Baba is within 100 ft of Layn for Echoing Strike.
- Baba's current action/reaction state when relevant.
- Whether Baba is taking a Help action or otherwise affecting an attack.
- Any current movement or positioning constraints.

Distances must be evaluated from the actual current battlefield position, not inferred from the previous turn.

## Darkness / carrier interaction

Layn has used a table-specific/homebrew tactic involving the Nightecho Stone changing into a trinket form, placing it in a closed palm, casting **Darkness** on it, tossing it, and having Baba catch/carry it so that Baba becomes the moving center of the Darkness effect.

This interaction is **homebrew/table-specific** and should be treated as an enabled campaign mechanic rather than a generic D&D rule.

## Independent stat block

The Nightecho Stone sheet does not provide Baba with an independent custom HP/AC/speed/attack stat block. The simulator should not invent one. If the table later establishes custom Baba statistics, record them here.
