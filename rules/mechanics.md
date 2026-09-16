# Mechanics Reference

## Resource pools

Track all limited resources explicitly.

### Psionic Energy Dice

At level 7: **6d8**.

- Psi-Bolstered Knack spends a die only if the added die turns the failed proficient skill/tool check into a success.
- Psychic Whispers consumes a die except for the first use after a Long Rest.
- Regain one die on Short Rest and all on Long Rest.

### Long-rest resources

- Faerie Fire: 1/day
- Darkness: 1/day
- Echoing Strike: 1/Long Rest

The simulator should track whether each has been spent.

## Reliable Talent

For an ability check using a skill or tool proficiency, natural d20 results 1–9 become 10.

This is **not** applied to:

- Attack rolls
- Saving throws
- Checks without the required proficiency

## Evasion

For an effect that permits a DEX save for half damage:

- Success -> 0 damage
- Failure -> half damage

Cannot be used while Incapacitated.

## Uncanny Dodge

Reaction when an attacker Layn can see hits with an attack roll: halve that attack's damage, rounding down.

Track whether Layn's Reaction is available before offering this option.

## Cunning Strike

When Layn deals Sneak Attack damage, Layn may forgo the listed number of Sneak Attack dice to add an effect.

At level 7 the available options are:

- Poison: forgo 1d6; CON save; Poisoned for 1 minute; requires Poisoner's Kit.
- Trip: forgo 1d6; DEX save; Prone on failure; Large or smaller.
- Withdraw: forgo 1d6; move up to half Speed without provoking Opportunity Attacks.

Do not offer Daze, Obscure, or Knock Out at level 7.

## Steady Aim and Bonus Action conflicts

Steady Aim costs a Bonus Action.

The Psychic Blade bonus attack also costs a Bonus Action.

Therefore Layn cannot use both on the same turn.

If Layn has already spent the Bonus Action, do not offer another Bonus Action ability.

## Sneak Attack once per turn

The simulator must maintain a per-turn Sneak Attack-used flag. Once applied, no later attack that turn may receive Sneak Attack.

## Familiar positioning

Baba's location is part of the combat state. Effects depending on Baba's distance must be evaluated against its current position at the instant of the relevant action/attack.

## Intelligence-aware enemies

Enemy behavior should be based on the creature's Intelligence, observed information, and available senses. Enemies should not automatically know Layn's position merely because the simulator knows it.

Intelligent enemies may deliberately Ready actions against expected movement or attacks when reasonable.
