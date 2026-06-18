# Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agentic QA Platform                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                       │
│  (To be implemented: Web UI, REST API, CLI)                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│              APPLICATION LAYER (src/main.py)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AgenticQAPlatform                                       │  │
│  │  - process_all_requirements()                            │  │
│  │  - process_single_requirement()                          │  │
│  │  - list_generated_test_cases()                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                 WORKFLOW ORCHESTRATION LAYER                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  QAWorkflow (LangGraph)                                  │  │
│  │                                                          │  │
│  │  1. parse_requirement  ───────┐                         │  │
│  │       ↓                        │                         │  │
│  │  2. extract_scenarios  ───────┤                         │  │
│  │       ↓                        │                         │  │
│  │  3. generate_test_cases ──────┤─→ RequirementAgent      │  │
│  │       ↓                        │    + LLM Integration    │  │
│  │  4. validate_output    ───────┤                         │  │
│  │       ↓                        │                         │  │
│  │  5. save_to_database   ───────┴→ Database Services      │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────┬────────────────────┬────────────────────────────┘
               │                    │
┌──────────────▼──────────┐   ┌─────▼──────────────────────────┐
│  AGENT LAYER            │   │  DATABASE SERVICE LAYER        │
│  ┌────────────────────┐ │   │  ┌──────────────────────────┐  │
│  │ Requirement Agent  │ │   │  │ RequirementService       │  │
│  │ - parse metadata   │ │   │  │ - create_requirement     │  │
│  │ - generate tests   │ │   │  │ - get_requirement        │  │
│  │                    │ │   │  │ - list_requirements      │  │
│  │ + OpenAI GPT-4     │ │   │  └──────────────────────────┘  │
│  │ + LangChain        │ │   │  ┌──────────────────────────┐  │
│  │ + LangSmith        │ │   │  │ TestCaseService          │  │
│  │                    │ │   │  │ - create_test_case       │  │
│  │ RequirementAnalyzer│ │   │  │ - update_status          │  │
│  │ - extract scenarios│ │   │  │ - list_test_cases        │  │
│  │ - extract criteria │ │   │  └──────────────────────────┘  │
│  └────────────────────┘ │   │  ┌──────────────────────────┐  │
│                         │   │  │ TestExecutionService     │  │
│  WORKFLOW FILE LAYER    │   │  │ - log_execution          │  │
│  ┌────────────────────┐ │   │  │ - get_executions         │  │
│  │RequirementFile     │ │   │  └──────────────────────────┘  │
│  │Processor           │ │   │                                │
│  │- get files         │ │   │ MODELS & SCHEMAS               │
│  │- save requirement  │ │   │ ┌──────────────────────────┐  │
│  └────────────────────┘ │   │ │ Pydantic Schemas         │  │
│                         │   │ │ - TestCaseSchema         │  │
│  (Future Agents)        │   │ │ - RequirementSchema      │  │
│  ┌────────────────────┐ │   │ │ - AgentState             │  │
│  │ Playwright Agent   │ │   │ └──────────────────────────┘  │
│  │ Defect Triage Agent│ │   └─────────────────────────────┘
│  │ Jira Integration   │ │
│  │ etc...             │ │
│  └────────────────────┘ │
└────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SQLAlchemy ORM (src/database/)                          │  │
│  │                                                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Requirements │  │  Test Cases  │  │  Executions  │  │  │
│  │  │              │  │              │  │              │  │  │
│  │  │ - id         │  │ - id         │  │ - id         │  │  │
│  │  │ - filename   │  │ - test_id    │  │ - test_id    │  │  │
│  │  │ - title      │  │ - title      │  │ - status     │  │  │
│  │  │ - content    │  │ - steps      │  │ - duration   │  │  │
│  │  │ - metadata   │  │ - precond.   │  │ - error_msg  │  │  │
│  │  │ - timestamps │  │ - priority   │  │ - logs       │  │  │
│  │  │              │  │ - status     │  │              │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │  SQLite Database (data/qa_platform.db)                   │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                    INPUT/OUTPUT LAYER                            │
│                                                                  │
│  INPUT:                              OUTPUT:                     │
│  ┌────────────────────────┐          ┌──────────────────────┐   │
│  │ Requirements (Markdown)│          │ Test Cases (JSON)    │   │
│  │ requirements_folder/   │          │ Database Tables      │   │
│  │ - *.md files          │          │ Logs (Log file)      │   │
│  └────────────────────────┘          │ Reports (TXT)        │   │
│                                      └──────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION & LOGGING                       │
│                                                                  │
│  Settings:              Logging:                                │
│  ┌─────────────────┐   ┌──────────────────────────────────┐    │
│  │ config/         │   │ logs/                            │    │
│  │ - settings.py   │   │ - app.log (rotating, 10MB max)  │    │
│  │ - logging.py    │   │ - Console output                │    │
│  │                 │   │ - File output                    │    │
│  │ Environment:    │   │ - Configurable level (INFO/DEBUG)│   │
│  │ - .env file     │   └──────────────────────────────────┘    │
│  │ - 15+ variables │                                            │
│  └─────────────────┘                                            │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────┐
│  Requirement Files  │
│ (Markdown format)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  RequirementFileProcessor               │
│  Reads .md files from requirements/     │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  LangGraph QA Workflow                  │
│  ┌─────────────────────────────────────┐│
│  │ 1. Parse Requirement                ││
│  │    Extract title, scope, requirements││
│  └────┬────────────────────────────────┘│
│       │                                  │
│  ┌────▼────────────────────────────────┐│
│  │ 2. Extract Scenarios                ││
│  │    Find user stories and criteria    ││
│  └────┬────────────────────────────────┘│
│       │                                  │
│  ┌────▼────────────────────────────────┐│
│  │ 3. Generate Test Cases              ││
│  │    → RequirementAgent (LLM)         ││
│  │    → OpenAI GPT-4                   ││
│  │    → LangChain/LangSmith            ││
│  └────┬────────────────────────────────┘│
│       │                                  │
│  ┌────▼────────────────────────────────┐│
│  │ 4. Validate Output                  ││
│  │    Check quality & completeness     ││
│  └────┬────────────────────────────────┘│
│       │                                  │
│  ┌────▼────────────────────────────────┐│
│  │ 5. Save to Database                 ││
│  │    Store test cases in SQLite       ││
│  └────┬────────────────────────────────┘│
└──────┼─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  SQLite Database                        │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │Reqs      │  │Test Cases│  │Execute││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Output & Reports                       │
│  - Test Cases (JSON)                    │
│  - Database Queries                     │
│  - Generated Reports                    │
│  - Logs                                 │
└─────────────────────────────────────────┘
```

## Component Interaction Diagram

```
User/CLI
   │
   ▼
AgenticQAPlatform (main.py)
   │
   ├─→ RequirementFileProcessor
   │   └─→ Load .md files
   │
   ├─→ QAWorkflow (LangGraph)
   │   ├─→ Node 1: parse_requirement()
   │   ├─→ Node 2: extract_scenarios()
   │   ├─→ Node 3: generate_test_cases()
   │   │   └─→ RequirementAgent
   │   │       ├─→ ChatOpenAI (LLM)
   │   │       └─→ LangSmith (Observability)
   │   ├─→ Node 4: validate_output()
   │   └─→ Node 5: save_to_database()
   │       ├─→ RequirementService
   │       └─→ TestCaseService
   │           └─→ SQLAlchemy ORM
   │               └─→ SQLite Database
   │
   ├─→ Database Services
   │   ├─→ RequirementService
   │   ├─→ TestCaseService
   │   └─→ TestExecutionService
   │
   └─→ Output & Reporting
       ├─→ Database Queries
       ├─→ Report Generation
       └─→ Logging
```

## Future Extension Points

```
Current Implementation:
├── Requirement Agent ✓
├── Test Case Generation ✓
├── Database Management ✓
└── Workflow Orchestration ✓

Planned Agents:
├── Playwright Agent
│   └── Browser Automation
├── Defect Triage Agent
│   └── Classification & Analysis
├── Jira Integration Agent
│   └── Defect Management
├── Performance Agent
│   └── Load Testing
└── Visual Testing Agent
    └── UI Validation

All agents will follow the same pattern:
1. Inherit from BaseAgent (future)
2. Integrate with QAWorkflow
3. Store results in appropriate tables
4. Use LangSmith for observability
```
