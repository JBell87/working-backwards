# Stage 4: Deliverables

After the spec has passed review, produce five documents in `docs/build/<slug>/`. They are how the user judges the plan at the approval gate without reading every plan file, and they stay in the repository as the system's documentation.

These documents describe the reviewed spec. They must not introduce anything new: no component, field, endpoint, or decision that is not already in `spec.md` or a plan. If writing one reveals a gap, fix the spec (and re-run the affected review pass) and regenerate; do not patch the gap in the document.

Write them yourself or dispatch one Standard-tier agent per document in a single message, each given `spec.md`, the plan files, and the locked PR/FAQ. Then check each against the spec.

## 1. `architecture.md`: architecture diagram

A Mermaid diagram of the components and how they connect, followed by one short paragraph per component saying what it is responsible for.

- Every box is an artifact from the spec; every arrow is a connection from the spec, labelled with what flows along it.
- Show the outside world: the customer, and any external service.
- Keep it to one diagram that fits on a screen. If it does not fit, draw one overview and one diagram per phase.

## 2. `schema.md`: data schema

Every piece of data the system stores: tables or collections, fields with types and constraints, keys, relationships, and indexes, with a Mermaid entity-relationship diagram when there is more than one entity. Include the data definition statements if the storage has them.

Also cover data that is stored outside a database: files the product writes, configuration it persists, formats it reads.

If the product stores nothing, say so in one line and describe the input and output formats it handles. Do not invent a database to fill the section.

## 3. `api.md`: interface reference

Every way the outside world talks to the product, in the form that fits it:

- HTTP or RPC service: each endpoint, with method, path, parameters, request and response bodies, status codes, errors, and an example.
- Command-line tool: each command and flag, with inputs, outputs, exit codes, and an example.
- Library: each public function or class, with signature, behaviour, errors, and an example.

Mark which truth each entry serves. An entry that serves no truth is scope creep; a truth with no entry point has no way to be observed.

## 4. `phases.md`: build phases

For each phase: the truths it delivers, what the customer will be able to do when it is finished, its plans grouped by wave with their criticality, and what it depends on. End with the totals: phases, plans, tasks, waves.

This is the document the user reads to decide whether the order and scope are right, so write the "what you will be able to do" lines in customer terms, not component terms.

## 5. `explained-simply.md`: the build explained to a kindergartener

A one-page explanation of what is being built and how, for a reader with no technical background at all. Short sentences, everyday words, one running comparison to something familiar (a lemonade stand, a library, a post office) carried all the way through.

Cover: who it is for and what problem they have, what the product does about it, the main parts and what each one's job is, and the order they get built in and why.

This is not a joke deliverable. If the build cannot be explained this simply, the design is not understood well enough, and the places where the simple explanation gets awkward are usually the places where the design is confused. Note any such place in the spec's decision log and reconsider it.

## Check before the approval gate

- Every name in every document appears in the spec, spelled the same way.
- The diagram, schema, and interface reference agree with each other (an endpoint that returns a field the schema does not have is a spec bug).
- `phases.md` totals match the plan files on disk.
- Commit the five documents together.
