# Attacks & Damage

## Attack resolution

For every attack:

1. Determine target and range.
2. Determine attack modifier.
3. Determine advantage/disadvantage.
4. Roll the appropriate d20 dice.
5. Apply character-specific modifiers such as Elven Accuracy or Mind's Fang when their conditions are met.
6. Compare the final result to target AC.
7. Resolve miss, hit, or critical hit.
8. On a hit, roll and log each damage component separately.
9. Apply on-hit effects and update temporary state.

## Layn's Psychic Blade

### Main blade

- Attack ability: Dexterity
- Attack modifier from DEX/PB: **+7** before other bonuses
- Weapon damage: **1d6 Psychic + 4**
- Finesse
- Thrown 60/120 ft
- Vex mastery

### Bonus blade

- Attack ability: Dexterity
- Attack modifier from DEX/PB: **+7** before other bonuses
- Weapon damage: **1d4 Psychic + 4**
- Requires the other hand to be free
- Uses Bonus Action after the main-blade attack

## Mind's Fang

When Baba is within 5 ft of the target, the Nightecho Stone's current sheet wording gives **+1d4 to attack rolls**.

This is an attack-roll modifier, not a damage die. Apply it to the attack roll only when its positional condition is satisfied.

## Sneak Attack

Layn can apply **4d6** Sneak Attack damage at most once per turn when the attack qualifies.

Log it as a separate damage component.

## Critical hits

A critical hit doubles the attack's applicable damage dice. The simulator should expand the individual dice rather than simply doubling the final numeric total, so that Savage Attacker and other mechanics can be resolved correctly.

## Savage Attacker

Once per turn when Layn hits with a weapon, Savage Attacker can reroll the weapon's damage dice and use either result.

For Psychic Blades:

- Main: reroll 1d6.
- Bonus: reroll 1d4.

Do not include Sneak Attack dice in the Savage Attacker reroll.

## Vex

After a Psychic Blade hits a target, mark that target as granting advantage on Layn's next attack against it, subject to the feature's duration. Consume the advantage when the qualifying next attack is made.

## Damage log format

Each hit should be representable as:

```text
Attack: Main Psychic Blade
Attack roll: 17 + 7 = 24 vs AC 16 -> Hit
Weapon: 1d6 -> 4
Ability modifier: +4
Sneak Attack: 4d6 -> 13
Familiar: +0 damage
Total: 21 Psychic
```

The exact values above are illustrative only; the simulator must use actual rolls and encounter state.
