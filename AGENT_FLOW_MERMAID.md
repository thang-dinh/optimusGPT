# Agent Flow Diagram - Mermaid Version

This document contains Mermaid diagrams that visualize the agent flow in optimusGPT. These diagrams will render automatically on GitHub and other platforms that support Mermaid.

## Overview Flow

```mermaid
graph TB
    Start([User Prompt<br/>Optimization Problem]) --> Initial[Path Initial<br/>First Iteration]
    Initial --> Output1{Output & Prompt<br/>User Decision}
    Output1 -->|Satisfied| End([Exit])
    Output1 -->|Not Satisfied<br/>Provide Feedback| Subsequent[Path Subsequent<br/>Iterative Flow]
    Subsequent --> Output2{Output & Prompt<br/>User Decision}
    Output2 -->|Satisfied| End
    Output2 -->|Not Satisfied<br/>More Feedback| Subsequent
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Initial fill:#fff9c4
    style Subsequent fill:#ffe0b2
```

## Initial Flow (First Iteration)

```mermaid
flowchart TD
    A([User Prompt]) --> B[Interpreter Agent<br/>gpt-4o-mini<br/><br/>Extract:<br/>- Objective<br/>- Variables<br/>- Constraints<br/>- Notes]
    B -->|structured_problem| C[Solver Agent<br/>gpt-4o-mini<br/><br/>Generate:<br/>- Python code<br/>- gurobipy model]
    C -->|generated_code| D[Code Execution<br/>PythonREPL<br/><br/>- Sanitize code<br/>- Execute 10s max<br/>- Return output]
    D -->|execution_output| E[Self-Check Agent<br/>gpt-4o-mini<br/><br/>Validate:<br/>- Correctness<br/>- Metrics<br/>- Implications]
    E -->|self_check_summary| F{User Decision<br/>Another iteration?}
    F -->|No| G([Exit])
    F -->|Yes<br/>Provide Feedback| H[Iterative Flow]
    
    style A fill:#e1f5ff
    style G fill:#c8e6c9
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#f3e5f5
    style E fill:#fff9c4
    style F fill:#ffccbc
    style H fill:#ffe0b2
```

## Iterative Flow (Subsequent Iterations)

```mermaid
flowchart TD
    A([User Feedback<br/>Additional Context]) --> B[Iterative Decision Agent<br/>gpt-4o-mini<br/><br/>Analyze:<br/>- Problem statement<br/>- Previous solution<br/>- Self-analysis<br/>- User feedback]
    B -->|decision| C{Next Step}
    
    C -->|1: Reinterpret| D[Interpreter Agent<br/>with feedback]
    D --> E[Solver Agent<br/>with reinterpretation]
    E --> F[Code Execution]
    
    C -->|2: Solve Again| G[Solver Agent<br/>with updated context]
    G --> F
    
    C -->|3: Request Info| H[Request More<br/>Information]
    H --> I[User Provides<br/>Additional Info]
    I --> J[Recursive Call<br/>path_subsequent<br/>with new context]
    J --> B
    
    F --> K[Self-Check Agent]
    K --> L{User Decision<br/>Another iteration?}
    L -->|No| M([Exit])
    L -->|Yes<br/>More Feedback| A
    
    style A fill:#e1f5ff
    style B fill:#fff9c4
    style C fill:#ffccbc
    style D fill:#fff9c4
    style E fill:#fff9c4
    style F fill:#f3e5f5
    style G fill:#fff9c4
    style H fill:#ffccbc
    style I fill:#e1f5ff
    style J fill:#ffe0b2
    style K fill:#fff9c4
    style L fill:#ffccbc
    style M fill:#c8e6c9
```

## Complete System with Feedback Loops

```mermaid
graph TB
    subgraph "Human-in-the-Loop Feedback"
        User([User]) -.->|Feedback| Decision[Decision Agent]
        Output -.->|Prompt for feedback| User
    end
    
    subgraph "Initial Iteration"
        I1[Interpreter<br/>Agent] --> S1[Solver<br/>Agent]
        S1 --> E1[Code<br/>Execution]
        E1 --> SC1[Self-Check<br/>Agent]
    end
    
    subgraph "Subsequent Iterations"
        Decision --> D{Strategy}
        D -->|Reinterpret| I2[Interpreter<br/>Agent]
        D -->|Solve Again| S2[Solver<br/>Agent]
        D -->|Need Info| Request[Request Info]
        Request -.->|Ask| User
        User -.->|Provide| Request
        Request --> D
        I2 --> S2
        S2 --> E2[Code<br/>Execution]
        E2 --> SC2[Self-Check<br/>Agent]
    end
    
    Start([Problem<br/>Statement]) --> I1
    SC1 --> Output[Output &<br/>Summary]
    SC2 --> Output
    Output --> End{Satisfied?}
    End -->|Yes| Exit([Complete])
    End -->|No| Decision
    
    style Start fill:#e1f5ff
    style Exit fill:#c8e6c9
    style User fill:#e1f5ff
    style Decision fill:#fff9c4
    style Output fill:#ffccbc
```

## Sequence Diagram (Interaction View)

```mermaid
sequenceDiagram
    participant U as User
    participant M as Main Flow
    participant IA as Interpreter Agent
    participant SA as Solver Agent
    participant E as Code Execution
    participant SC as Self-Check Agent
    participant DA as Decision Agent
    
    U->>M: Submit Problem
    activate M
    M->>IA: Parse Problem
    activate IA
    IA-->>M: Structured Problem
    deactivate IA
    
    M->>SA: Generate Code
    activate SA
    SA-->>M: Python Code
    deactivate SA
    
    M->>E: Execute Code
    activate E
    E-->>M: Results
    deactivate E
    
    M->>SC: Validate Solution
    activate SC
    SC-->>M: Quality Summary
    deactivate SC
    
    M-->>U: Output & Results
    U->>U: Review
    
    alt User Not Satisfied
        U->>M: Provide Feedback
        M->>DA: Analyze Feedback
        activate DA
        DA-->>M: Strategy Decision
        deactivate DA
        
        alt Reinterpret Problem
            M->>IA: Reinterpret with Feedback
            activate IA
            IA-->>M: New Interpretation
            deactivate IA
            M->>SA: Generate New Code
            activate SA
            SA-->>M: Updated Code
            deactivate SA
        else Solve with Context
            M->>SA: Solve with Updated Context
            activate SA
            SA-->>M: Updated Code
            deactivate SA
        else Request More Info
            M->>U: Request Additional Info
            U->>M: Provide Info
            M->>DA: Re-analyze with New Info
        end
        
        M->>E: Execute Updated Code
        activate E
        E-->>M: New Results
        deactivate E
        
        M->>SC: Validate New Solution
        activate SC
        SC-->>M: New Summary
        deactivate SC
        
        M-->>U: Updated Output
    end
    
    deactivate M
```

## State Diagram (Agent States)

```mermaid
stateDiagram-v2
    [*] --> Initial: User Prompt
    
    Initial --> Interpreting: path_initial()
    Interpreting --> Solving: structured_problem
    Solving --> Executing: generated_code
    Executing --> SelfChecking: execution_output
    SelfChecking --> AwaitingFeedback: self_check_summary
    
    AwaitingFeedback --> [*]: User Satisfied
    AwaitingFeedback --> Deciding: User Provides Feedback
    
    Deciding --> Reinterpreting: Decision: Reinterpret
    Deciding --> ResolvingContext: Decision: Solve Again
    Deciding --> RequestingInfo: Decision: Need Info
    
    Reinterpreting --> Solving: new_interpretation
    ResolvingContext --> Solving: updated_context
    
    RequestingInfo --> AwaitingUserInfo: request_details
    AwaitingUserInfo --> Deciding: user_provides_info
    
    Solving --> Executing
    Executing --> SelfChecking
    SelfChecking --> AwaitingFeedback: iteration_complete
    
    note right of Deciding
        Iterative Decision Agent
        analyzes previous attempts
        and user feedback
    end note
    
    note right of AwaitingFeedback
        Human-in-the-Loop
        feedback collection
    end note
```

## Component Diagram (Architecture View)

```mermaid
graph TB
    subgraph "Agent Framework"
        subgraph "Core Agents"
            IA[Interpreter Agent<br/>structured output]
            SA[Solver Agent<br/>code generation]
            SCA[Self-Check Agent<br/>validation]
            DA[Decision Agent<br/>strategy selection]
        end
        
        subgraph "Execution Layer"
            REPL[PythonREPL<br/>code execution]
        end
        
        subgraph "Orchestration"
            PI[path_initial<br/>first iteration]
            PS[path_subsequent<br/>iterative flow]
        end
    end
    
    subgraph "External Components"
        LLM[LLM Provider<br/>gpt-4o-mini]
        User[User Interface]
        File[File System<br/>generated_code.py]
    end
    
    User --> PI
    User -.-> PS
    
    PI --> IA
    PI --> SA
    PI --> REPL
    PI --> SCA
    
    PS --> DA
    PS --> IA
    PS --> SA
    PS --> REPL
    PS --> SCA
    
    IA --> LLM
    SA --> LLM
    SCA --> LLM
    DA --> LLM
    
    SA --> File
    REPL --> File
    
    PI --> User
    PS --> User
    
    style IA fill:#fff9c4
    style SA fill:#fff9c4
    style SCA fill:#fff9c4
    style DA fill:#fff9c4
    style REPL fill:#f3e5f5
    style User fill:#e1f5ff
    style LLM fill:#e8eaf6
```

## Feedback Loops Visualization

```mermaid
graph LR
    subgraph "Primary Feedback Loop"
        U1[User] -->|Feedback| D1[Decision Agent]
        D1 --> S1[Strategy]
        S1 --> A1[Agents]
        A1 --> O1[Output]
        O1 -->|Prompt| U1
    end
    
    subgraph "Information Gathering Loop"
        D2[Decision Agent] -->|Need Info| R[Request]
        R -->|Ask| U2[User]
        U2 -->|Provide| D2
    end
    
    subgraph "Agent Chaining"
        I[Interpreter] --> So[Solver]
        So --> E[Execution]
        E --> SC[Self-Check]
        SC --> De[Decision]
        De -.->|Next Iteration| I
    end
    
    style U1 fill:#e1f5ff
    style U2 fill:#e1f5ff
    style D1 fill:#fff9c4
    style D2 fill:#fff9c4
    style A1 fill:#fff9c4
    style O1 fill:#ffccbc
```

## Data Flow Diagram

```mermaid
flowchart LR
    A[User Prompt] -->|text| B[Interpreter Agent]
    B -->|JSON schema| C[Solver Agent]
    C -->|Python code| D[Code Sanitizer]
    D -->|clean code| E[PythonREPL]
    E -->|stdout/result| F[Self-Check Agent]
    F -->|summary text| G[Output]
    G -->|display| H[User]
    H -->|feedback text| I[Decision Agent]
    I -->|strategy + context| C
    I -->|reinterpret| B
    I -->|request| H
    
    style A fill:#e1f5ff
    style B fill:#fff9c4
    style C fill:#fff9c4
    style D fill:#f3e5f5
    style E fill:#f3e5f5
    style F fill:#fff9c4
    style G fill:#ffccbc
    style H fill:#e1f5ff
    style I fill:#fff9c4
```

---

## How to View These Diagrams

### On GitHub
These Mermaid diagrams will render automatically when viewing this file on GitHub.

### In VS Code
Install the "Markdown Preview Mermaid Support" extension to see live previews.

### Online Editors
Copy the Mermaid code to:
- https://mermaid.live for live editing and export
- https://mermaid.ink for quick rendering

### Export Options
From mermaid.live, you can export to:
- PNG (for documentation)
- SVG (for scalable graphics)
- PDF (for reports)

### Integration
These diagrams can be:
- Embedded in README.md
- Included in documentation sites
- Exported for presentations
- Version controlled with code
