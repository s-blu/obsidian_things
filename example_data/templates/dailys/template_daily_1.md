---
day: %filename%
wellbeing:
  mood: %number;;%
  mood-notes: %text;discomfort|relaxed|sad|happy|neutral|euphoric|heartbroken|happy|sad|neutral|neutral|neutral|%
  health: %number;3;%
  health-notes: %text;good!|tired|okay|slight headaches right side%
  pain: %number;0;2%
  pain-type: %text;||||back|legs%
---
#daily #journal

# Daily Note %filename%

- [ ] Task 1 of %filename%
- [x] Completed Task of %filename%
- [%text;-|x|x|x|x| |>|o%] Task with state (maybe)
- [%text;-|x|x|x|x| |>|o%] Task with state (maybe) 2
- [%text;-|x|x|x|x| |>|o%] Task with state (maybe) 3
- [%text;-|x|x|x|x| |>|o%] Task with state (maybe) 4
- [%text;-|x|x|x|x| |>|o%] Task with state (maybe) 5

Today I ate [icecream:: %number;0;3%] and [buns:: %number;;%].

#### Appointments
My next appointment with [person:: %text;Lisa|Paul|AB1908|Christa|Fernando|Elias%] is on [appointment:: %date;filename;%].
Also I have an appointment at [appointment:: %date;filename;% %time;;%] with [person:: %text;Bob|Alice|Karl|Jonathan|Barbara%]

#### Metadata

**Daily Routine**
wake-up:: %time;06:00;08:23%
lunch:: 12:00
dinner:: %time;15:00;%
go-to-sleep:: %time;21:45;23:55%

**Workout**
training:: %text;15m|1h 5m|23m|1h 27m|36m|%
situps:: %number;0;25%
steps:: %number;35;11183%

**Good habits**
praying:: %text;yes|%
breathing:: %text;yes|%
beingthankful:: %text;yes|%
slowdown:: %text;yes|%
