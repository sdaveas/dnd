# Combat Rules — Simulation Layer

This file defines the generic combat state the battle simulator must maintain.

## Initiative

Every combatant rolls initiative and receives an initiative position.

A creature that is surprised still has an initiative position. Surprise affects what it can do on its first turn; it does not create a separate second turn for the attacker.

## Turn state

For every creature, track:

- Initiative position
- Current HP / maximum HP
- Current position
- Movement / remaining Speed
- Action availability
- Bonus Action availability
- Reaction availability
- Conditions
- Concentration where relevant
- Temporary effects and durations
- Resource pools
- Hidden/visible state
- Known/unknown location where relevant

## Action economy

A creature generally has one Action and one Bonus Action on its turn when applicable, plus movement and one Reaction between the start of its turn and the start of its next turn.

Never silently allow two Bonus Actions in the same turn.

## Opportunity attacks

Track movement through threatened areas and whether an effect allows movement without provoking an Opportunity Attack.

## Saving throws

Always record:

- Saving throw ability
- Target's save modifier
- DC
- Natural d20 result
- Final result
- Whether the effect is negated, reduced, or applied

## Attack rolls

Always record:

- Attack type/source
- Target
- Attack modifier
- Advantage/disadvantage state
- Dice rolled
- Final attack result
- Target AC
- Hit/miss/critical result

## Advantage/disadvantage

Track advantage and disadvantage as combat state. Under the normal rule, multiple sources do not stack; advantage and disadvantage cancel each other before rolling.

Character-specific mechanics such as Elven Accuracy can modify how an advantage roll is made.

## Hidden and known location

These are separate state variables.

A creature can be hidden while its location is known or unknown depending on the circumstances. Do not collapse these states into a single boolean.

## Monster AI

Enemy decisions should respect the creature's Intelligence and available information.

Intelligent enemies may:

- Infer likely locations from observed actions.
- Ready actions when appropriate.
- Focus vulnerable targets.
- Use known information rather than omniscient information.

Do not give enemies information they have not obtained.

## Ready actions

When an intelligent creature has a trigger it could reasonably anticipate, it may Ready an action. Record the trigger and the held action as explicit state until it fires or becomes invalid.

## Reaction state

Track reaction availability separately for every combatant. Reactions are not automatically restored after every attack; restoration follows the applicable rules.

## Spatial state

Use exact distances whenever a mechanic depends on distance. At minimum track:

- Position
- Distance between relevant creatures
- Line of sight where relevant
- Areas/effects occupying space
- Carried/moving effect origins where applicable
