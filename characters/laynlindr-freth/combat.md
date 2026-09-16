# Layn — Combat Profile

This file describes combat-specific behavior and state that the simulator should track.

## Action economy

Track separately each turn:

- Action
- Bonus Action
- Reaction
- Movement / remaining Speed
- Free object interaction where relevant

The Psychic Blade bonus attack consumes the Bonus Action, so Layn cannot also use Cunning Action or Steady Aim in the same turn.

## Attack sequence

A standard two-blade sequence is:

1. Attack with the main Psychic Blade.
2. If desired and the other hand is free, make the bonus Psychic Blade attack using the Bonus Action.

Each Psychic Blade attack has its own attack roll and damage roll.

## Advantage and Elven Accuracy

When Layn has advantage on a Dexterity-based attack, use **3d20 and take the highest** under Elven Accuracy.

Do not apply Elven Accuracy when Layn merely has a normal attack or when the attack is not a qualifying Dexterity attack.

## Vex tracking

After a Psychic Blade hits a target, the next attack against that target has advantage. Track this as a per-target temporary combat state and consume it when the qualifying next attack is made.

## Sneak Attack policy

Sneak Attack can be applied only once per turn.

When multiple attacks qualify, the player chooses which attack receives the Sneak Attack dice.

Default player doctrine:

- Usually hold Sneak Attack for the bonus Psychic Blade.
- If the main attack is a critical hit, normally apply Sneak Attack to that critical hit instead.
- Do not treat this doctrine as a mandatory rule; it is a decision policy.

## Savage Attacker

When used after a weapon hit, reroll the weapon's damage dice and use either result. It affects the weapon damage dice, not Sneak Attack dice.

For Psychic Blades this means:

- Main blade: reroll the 1d6 weapon die.
- Bonus blade: reroll the 1d4 weapon die.
- Do not reroll Sneak Attack's 4d6 through Savage Attacker.

## Damage accounting

For every successful attack, keep damage components separate:

1. Weapon die
2. Ability modifier
3. Sneak Attack dice, if applied
4. Familiar/item bonus, if applicable
5. Any other explicit effect

This makes combat logs auditable and allows exact post-combat damage analysis.

## Critical hits

On a critical hit, double the attack's damage dice according to the applicable rules. Keep each component explicit in the combat log.

## Reactions

Track whether the Reaction has been spent each round/turn as applicable.

Primary Layn defensive reaction:

- **Uncanny Dodge:** when an attacker Layn can see hits with an attack roll, halve that attack's damage.

## Movement and stealth

Track exact positions and distances rather than only adjacency.

Track these separately:

- Hidden / not hidden
- Known location / unknown location
- Line of sight
- Distance to each creature
- Baba's position

Do not equate being unseen with an automatically unknown location unless the applicable rules establish it.
