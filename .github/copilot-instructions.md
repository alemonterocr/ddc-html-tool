# GitHub Copilot Workspace Instructions

You are an expert Software Engineer. When generating code, answering questions, or refactoring in this workspace, you must adhere strictly to the following architectural and stylistic constraints:

## 1. Architectural Patterns (No Shortcuts)

- **Data Access:** Enforce the **Repository Pattern**. Never put raw database queries or ORM calls directly inside controllers or business logic.
- **Business Logic:** Favor the **Strategy Pattern** over massive `switch` or `if/else` chains. If behavior changes based on a type, abstract it into a strategy interface.
- **Object Creation:** Use **Factory Methods** or Dependency Injection containers for complex object creation. Do not use the `new` keyword scattered throughout business logic.

## 2. Applied SOLID Principles (Concrete Rules)

- **Single Responsibility:** A function must do exactly one thing. If you find yourself writing "and" in the function's description, break it into smaller private methods.
- **Open/Closed:** Design features so we can add new functionality by adding new files, not by modifying existing core files. Use Composition over Inheritance.
- **Dependency Inversion:** Always depend on abstractions (Interfaces/Types), not concrete implementations. **All dependencies must be injected via constructors.**

## 3. Code Quality & State Management

- **Immutability:** Default to immutable data structures. Never mutate input parameters. (e.g., Use `const`, `readonly`, or immutable array methods like `map`/`filter`).
- **Fail Fast:** Validate inputs at the very top of a function and throw exceptions early. Do not nest core logic inside deep `if` blocks.
- **Error Handling:** Never swallow errors with empty `catch` blocks. Always catch specific error types, wrap them in custom application errors, and include contextual logging.

## 4. Testing Requirements

- When asked to write tests, use the **Arrange, Act, Assert (AAA)** pattern.
- Mock external dependencies and database calls. Do not mock the system under test.
- Focus on testing behaviors and outcomes, not private internal methods.
