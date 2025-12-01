% Define actions
action(scanarea).
action(moveforward).
action(pickobject).

% Preconditions
precondition(scanarea, true).
precondition(moveforward, path_clear).
precondition(pickobject, object_detected).

% World knowledge (mocked)
world(path_clear).
world(object_detected).

% Validation
validate(A, "valid") :-
    action(A),
    precondition(A, Cond),
    world(Cond), !.

validate(_, "invalid_action") :-
    fail.
validate(A, "precondition_failed") :-
    action(A).
