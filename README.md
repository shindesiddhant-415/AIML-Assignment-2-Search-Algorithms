# AIML Practical 2 - Search Algorithms

## Performance Evaluation of Uninformed, Informed, Local Search and Constraint Satisfaction Algorithms

This practical implements and evaluates four Artificial Intelligence problem-solving techniques using different problem scenarios.

The algorithms implemented are:

- Breadth First Search (BFS)
- A* Search
- Hill Climbing
- Constraint Satisfaction Problem (CSP)

The implementations are written in Python and executed using Google Colab.

---

## Problem Statement

To implement and evaluate different Artificial Intelligence search techniques including Uninformed Search, Informed Search, Local Search, and Constraint Satisfaction techniques.

Different problem scenarios are used for each technique:

- BFS → Campus navigation from Gate to Auditorium
- A* → Weighted campus navigation using heuristic values
- Hill Climbing → Mathematical function maximization
- CSP → Examination timetable scheduling

The algorithms are evaluated using parameters such as nodes explored, execution time, solution quality, and applicability.

---

## Objectives

1. Implement different AI search techniques in Python.
2. Understand the working of BFS, A*, Hill Climbing and CSP.
3. Compare the performance of the implemented algorithms.
4. Analyze the suitability of each algorithm for different problem-solving situations.

---

## Algorithms Used

### 1. Breadth First Search (BFS)

BFS is an uninformed search algorithm that explores nodes level by level.

In this practical, BFS is used to find a route from the **Gate** to the **Auditorium** in a campus graph.

---

### 2. A* Search

A* is an informed search algorithm that uses both the actual path cost and a heuristic value.

It uses the evaluation function:

```text
f(n) = g(n) + h(n)
