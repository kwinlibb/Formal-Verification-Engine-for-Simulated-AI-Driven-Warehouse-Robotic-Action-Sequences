% Define actions
action(scanarea).
action(moveforward).
action(pickobject).

% Preconditions
precondition(scanarea, true).
precondition(moveforward, path_clear).
precondition(pickobject, object_detected).

% World knowledge (mocked)
world(true).
world(path_clear).
world(object_detected).

% Validation
validate(A, "invalid_action") :-
    \+ action(A), !.

validate(A, "precondition_failed") :-
    action(A),
    precondition(A, Cond),
    \+ world(Cond), !.

validate(A, "valid") :-
    action(A),
    precondition(A, Cond),
    world(Cond), !.
