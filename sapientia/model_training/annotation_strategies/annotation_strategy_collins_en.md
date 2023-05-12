# Collins - Annotation strategy 

This document summarizes the annotation strategy for Collins training data. 

## Named entities

We identified the following named entities : 

- ORG
- ROLE
- DOCUMENT
- STANDARD
- CRITERIA
- COMPONENT
- HARDWARE
- SYSTEM
- PARAMETER
- CONDITION
- UNIT
- PROCESS
- EVENT
- PHASE
- LANGUAGE


### Org 

Used to represent organisations such as Airbus or Collins.

### Role 

Roles are given to entities such as the _Supplier_, the _Provider_, or the _equipment manufacturer_, for example. 

### Document

Used to describe documents such as _technical reports_ or _technical specifications_.

### Standard

Standards are norms such as _DO-178C_.

### Criteria

Criteria are requirements such as _maintainability_ or _safety_.

### Component

A component is a hardware part such as _Electro-Mechanical Actuator_. 

### Hardware

_Aircraft_ is not a component, it's hardware.

### System

We also need to describe systems such as _flight control system_.

### Parameter

Internal variables and features such as _life time_, _coefficient degradation_. or _input power_, as well as external parameters such as _temperature_.

### Condition

Used to describe the state of a component or an operating condition, for example _active_, _true_, _in-flight_ or _open_.

### Unit

Units are used to precisely describe measures such as temperatures (_11°C_), distance (_3cm_) or voltage, for example.

### Process

Processes are operations such as _monitoring_, for example.

### Event

External events that alter a component or a system condition or parameter, typically _failures_, for example.

### Phase

Project phases such as _design_, _development_ or _rig tests_.

### Language

Natural languages such as _English_ or _French_.

## Relations

We identified the following relations : 

- COLLABORATION
- PROVIDE
- DEFINED_BY
- COMPLY_WITH
- COMPOSED_BY
- HAS_FEATURE
- HAS_VALUE
- PERFORM
- SUBJECT
- COMMUNICATE
- IN_CONDITION
- IN_PHASE
- CONTROL
- CONNECTION

The relations are directed, except for CONNECTION and COLLABORATION. We use the following notation : relation(named_entity_1, named_entity_2) to represent the relation from named_entity_1 to named_entity_2.

### Collaboration

_Collaboration_ is a relation existing between two roles. 

For example, the _Supplier_ **works** on the technical specification with the _Provider_.

COLLABORATION(Supplier, Provider)

_Collaboration_ is one of the few undirected relations.

### Provide

_Provide_ is a relation existing between a role and a standard, document, hardware, system, component, phase or process.
,
For example, the _Supplier_ **provides** _technical requirements_ to the _Provider_. 

PROVIDE(Supplier, technical requirements)

It should be noted that there exists a relations between _technical requirements_ and _Provider_ (SUBJECT).

### Defined by

Defined by is a relation existing between standard and a document.

For example, the _specific requirements_ are **defined** in the _technical specification_.

DEFINED_BY(specific requirements, technical specification)

### Comply with

_Comply with_ is a relation existing between an entity and a standard.

For example, the _technical specification_ **complies with** the _DO-178C_ norm.

COMPLY_WITH(technical specification, DO-178C)

### Composed by

_Composed by_ is a relation existing between two components, a system and its components, or hardware and one of its systems or components. 

For example, the _aircraft_ is **composed by** the _electro-mechanical actuator_ among other components.

COMPOSED_BY(aircraft, electro-mechanical actuator)

### Has feature

_Has feature_ is a relation existing between hardware, a system or a component and a parameter.

For example, the _sensor_ **has a** _temperature_ of 11°C.

HAS_FEATURE(sensor, temperature)

### Has value

_Has value_ is a relation existing between a parameter and a unit.

For example, the sensor has a _temperature_ **of** _11°C_.

HAS_VALUE(temperature, 11°C)

### Perform

_Perform_ is a relation existing between hardware, a system or a component and a process.

For example, the _sensor_ **performs** temperature monitoring.

PERFORMS(sensor, temperature monitoring)

### Subject

_Subject_ is a relation existing between a process and a parameter.

For example, the sensor _monitors_ _temperature_.

SUBJECT(monitors, temperature)

### Communicate

_Communicate_ is a relation existing between two hardware, systems or components.

For example, the _data bus_ **sends messages** to the _actuator_.

COMMUNICATES(data bus, actuator)

### In condition

_In condition_ is a relation existing between a composant, a system or a hardware and a condition. 

For example, the _door_ **is** _open_.

IN_CONDITION(door, open)

### In phase

_In phase_ is a relation existing between a composant, a system or a hardware and a phase. 

For example, the _EMEA_ had no functioning issue **under** _test_.

IN_PHASE(EMEA, test)

### Control

Control is a relation existing between components, systems or hardware.

For example, the _electro-hydraulic servo valves_ **control** the movement of the _actuators_.

CONTROL(electro-hydraylic servo valves, actuators)

### Connection

Connection is a relation existing between two components that are physically connected.

