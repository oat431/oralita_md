# Code smell and Heuristics

## Comments
- Inappropriate Information
- Obsolete comment
- Redundant Commnet
- Poorly Written Comment
- Commented-out Code

## Environment
- Build requires more than one step
- Test require more than one step

## Functions
- Too many arguments
- Output Arguments
- Flag Arguments
- Dead Function

## General
- Multiple Languages in one source file
- Obvious Behavior is unimplmented
- Incoorect Behavior at the boundaries
- Overridden Safeties
- Duplication
- Code at Wrong Level of Abstraction
- Base classes depending on their derivatives
- Too much information
- Dead code
- Vertical separation
- Inconsistency
- Clutter
- Artificial Coupling
- Feature Envy
- Selector arugments
- Obscured intent
- Misplaced Responsiblity
- Inappropriate static
- Use Explanatory Variables
- Funcation name should say what they do
- Undersatnd the algorithm
- Make logical dependencies physical
- Prefer polymorphism to if/else or switch/case
- Follow standard conventions
- Replace magic number with named constants
- Be precise
- Structure over Convention
- Encapsulate conditionals
- Avoid negative conditionals
- Funcations should do one thing
- Hidden temporal compulings
- Don't be arbitrary
- Encapsulate boundary conditions
- Functions should descend only one level of abstraction
- Keep configurable data at high leavels
- Avoid transitive navigation

## Enterprise Framework
- Avoid long import list by using wildcards
- Don't Inherit Constants
- Constants vs Enuums

## Names
- Choose Descriptive names
- Choose Names at the appropriate level of abstraction
- Use standard nomenclature where possible
- Unambigous names
- Use long names for long scopes
- Avoid Encodings
- Name should describe side-effects

## Tests
- Insufficient tests
- Use a coverate tool
- Don't skip trivial tests
- An ingonored test is a question about an ambiguity
- Test boundary conditions
- Exhaustively test near bugs
- Patterns of failure are revealing
- Test coverage patterns can be revaling
- Test should be fast