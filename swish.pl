:- dynamic cell/3.
:- dynamic dim/3.
:- dynamic visited/2.

% Facts for knowledge base
% cell(X, Y, Type) represents the contents of a cell:
% Type can be 'home', 'pit', 'gold', 'breeze, 'glitter', or 'empty'

adjacent(X1, Y1, X2, Y2) :-
    (X2 is X1+1, Y2 is Y1);
    (X2 is X1-1, Y2 is Y1);
    (X2 is X1, Y2 is Y1+1);
    (X2 is X1, Y2 is Y1 - 1).

withinthewall(X,Y):-
    dim(Dim),
    X >= 0,
    Y >= 0,
    X =< Dim,
    Y =< Dim.
    
addsafe(X,Y):-
    not(cell(X,Y,safe)),assertz(cell(X,Y,safe)),
    (cell(X,Y,unknown),retract(cell(X,Y,unknown))).
    
addunsafe(X,Y):-
    not(cell(X,Y,unsafe)),assertz(cell(X,Y,unsafe)),
    (cell(X,Y,unknown),retract(cell(X,Y,unknown))).

addunknown(X,Y):-
    not(cell(X,Y,unknown)),assertz(cell(X,Y,unknown)).

safe(X, Y):-
    cell(X,Y,safe),not(cell(X,Y,breeze)),
    (
    ((AX is X+1,(withinthewall(AX, Y)),addsafe(AX, Y));!),
    ((BX is X-1,(withinthewall(BX, Y)),addsafe(BX, Y));!),
    ((AY is Y+1,(withinthewall(X, AY)),addsafe(X, AY));!),
    ((BY is Y-1,(withinthewall(X, BY)),addsafe(X, BY));!)
    ).

checkup(X,Y):-
    cell(X,Y,breeze),
    AX is X+1,(not(withinthewall(AX,Y));cell(AX,Y,safe)),
    BX is X-1,(not(withinthewall(BX,Y));cell(BX,Y,safe)),
    AY is Y+1,(not(withinthewall(X,AY));cell(X,AY,safe)).

checkdown(X,Y):-
    cell(X,Y,breeze),
    AX is X+1,(not(withinthewall(AX,Y));cell(AX,Y,safe)),
    BX is X-1,(not(withinthewall(BX,Y));cell(BX,Y,safe)),
    BY is Y-1,(not(withinthewall(X,BY));cell(X,BY,safe)).

checkleft(X,Y):-
    cell(X,Y,breeze),
    BX is X-1,(not(withinthewall(BX,Y));cell(BX,Y,safe)),
    AY is Y+1,(not(withinthewall(X,AY));cell(X,AY,safe)),
    BY is Y-1,(not(withinthewall(X,BY));cell(X,BY,safe)).

checkright(X,Y):-
    cell(X,Y,breeze),
    AX is X+1,(not(withinthewall(AX,Y));cell(AX,Y,safe)),
    AY is Y+1,(not(withinthewall(X,AY));cell(X,AY,safe)),
    BY is Y-1,(not(withinthewall(X,BY));cell(X,BY,safe)).

unsafe(X, Y):-
    cell(X,Y,unknown),
    (AX is X+1,checkright(AX,Y);
    BX is X-1,checkleft(BX,Y);
    AY is Y+1,checkup(X,AY);
    BY is Y-1,checkdown(X,BY)).

%Unknown cells
unknown(X, Y):-
    cell(X,Y,breeze),
    AX is X+1,not(cell(AX,Y,safe)),not(cell(X,Y,unknown)),assertz(cell(X,Y,unknown));
    BX is X-1,not(cell(BX,Y,safe)),not(cell(X,Y,unknown)),assertz(cell(X,Y,unknown));
    AY is Y+1,not(cell(X,AY,safe)),not(cell(X,Y,unknown)),assertz(cell(X,Y,unknown));
    BY is Y-1,not(cell(X,BY,safe)),not(cell(X,Y,unknown)),assertz(cell(X,Y,unknown)).

yesbreeze(X, Y) :-
    cell(X, Y, breeze).

yesglitter(X, Y) :-
    cell(X, Y, gold),
    not(cell(X, Y, grabbed)).

yesboth(X, Y) :-
    yesglitter(X, Y),
    yesbreeze(X, Y).
    
%Reset visited
reset_game :-
    retractall(visited(_, _)).
