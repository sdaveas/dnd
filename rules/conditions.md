# Conditions & Combat States

The simulator should represent conditions explicitly rather than as free-form notes.

## Prone

Track Prone as a condition with its normal effects on attacks and movement. Layn's Cunning Strike **Trip** can impose Prone after a failed DEX save on a Large-or-smaller target.

## Poisoned

Track Poisoned as a condition. Layn's Cunning Strike **Poison** can impose Poisoned for 1 minute after a failed CON save, provided the Poisoner's Kit requirement is met.

## Charmed

Layn has Fey Ancestry, granting advantage on saving throws to avoid or end the Charmed condition.

## Incapacitated

Track Incapacitated explicitly because Layn's Evasion cannot be used while Incapacitated.

## Hidden

Track whether a creature is currently hidden separately from whether other creatures know its location.

## Invisible / unseen

Track visibility independently from known location. Do not infer a creature's exact location solely from visibility state.

## Temporary effects

Every temporary effect should record:

- Source
- Target
- Start time/turn
- Duration
- Trigger for ending, if any
- Whether it has been consumed

## Darkness

Darkness is an area/effect with a location and radius rather than a property of a creature. Track its origin and movement explicitly.

Layn's table-specific Nightecho Stone/Baba carrier interaction is documented in `companions/baba.md` and must be treated as homebrew rather than a generic rule.
