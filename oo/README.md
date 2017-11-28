# Object-oriented Solution

This solution attempts to build a truly object-oriented solution to the elevator problem.
It follows the ideas laid out in [East-Oriented Design][east]
and [Object Calisthenics][cali].

## East Oriented Design

East Oriented Design is a guide
for how to design how your objects communicate.
James Ladd came up with it,
and describes it like this:

> Objects can flow in many directions
> and the design and structure of the code dictates these directions.
> The four points of the compass can be applied to the structure
> and execution
> of program code.
> When looking at the code on paper
> or screen
> you find North is up a layer,
> South is down a layer,
> West is left away from an object,
> and East is right towards another object.

He goes on to say:

> The East approach is the structuring of code to an East orientation.
> The rigorous application of this East principle decreases coupling
> and the amount of code that needs to be written,
> whilst increasing the clarity,
> cohesion,
> flexibility,
> reuse and testability of that code.
> It is easier to create a good design,
> structure,
> and identify dependencies and abstractions
> by simply orienting East.

## Object Calisthenics

Object Calisthenics is a set of strict design guidelines
that are intended to help you create truly object-oriented solutions.
By that I mean solutions that follow the intent the creators of object-oriented programming had in mind.
And that means those solutions should therefore get all of the benefits of object-oriented programming.

* Only One Level Of Indentation Per Method
* Don’t Use The ELSE Keyword
* Wrap All Primitives And Strings
* First Class Collections
* One Dot Per Line
* Don't Abbreviate
* Keep All Entities Small
* No Classes With More Than Two Instance Variables
* No Getters/Setters/Properties

## POODR

There's one more idea I'm trying to follow in this code.
It's an idea proposed by Sandi Metz
in her [POODR][metz] book:

> "...blind trust is a keystone of object-oriented design.
> It allows objects to collaborate
> without binding themselves to context
> and is necessary in any application that expects to grow and change.
> [...]
> When messages are trusting
> and ask for what the sender wants
> instead of telling the receiver how to behave,
> objects naturally evolve public interfaces that are flexible and reusable
> in novel and unexpected ways."

She goes on to mention three types of interactions
from the calling object's perspective:

> 1. "I know what I want and I know how you do it."
> 2. "I know what I want and I know what you do."
> 3. "I know what I want and I trust you to do your part."

The third is what you're aiming for
in good OO design.
It's what I'm aiming for here.

<!-- References -->
[cali]: http://jamesladdcode.com/2017/02/03/object-calisthenics/
[east]: http://jamesladdcode.com/2007/02/02/draft-design-compass-east/
[metz]: http://www.poodr.com/
