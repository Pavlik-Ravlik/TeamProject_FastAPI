# TeamProject_FastAPI
Цей додаток - це REST API на базі FastAPI, який дозволяє користувачам завантажувати, керувати та коментувати світлини. Його головною метою є створення платформи для спільного обміну та взаємодії користувачів зображеннями та коментарями, з можливістю аутентифікації користувачів та керування доступом до функцій, включаючи різні ролі користувачів (звичайний користувач, модератор і адміністратор).

## Вступ

У цьому проекті реалізовано REST API на базі FastAPI для управління світлинами, аутентифікацією користувачів та коментуванням.

## Аутентифікація

- Для аутентифікації користувачів використовується JWT-токени.
- Є три ролі користувачів: звичайний користувач, модератор і адміністратор. Перший користувач завжди адміністратор.
- Для забезпечення різних рівнів доступу, використовуються декоратори FastAPI для перевірки токенів і ролей користувачів.

## Робота зі світлинами

- Користувачі можуть завантажувати світлини з описом (POST).
- Користувачі можуть видаляти світлини (DELETE).
- Користувачі можуть редагувати опис світлини (PUT).
- Користувачі можуть отримувати світлини за унікальним посиланням (GET).
- Можливість додавати до 5 тегів під світлину.
- Теги унікальні для всього застосунку і створюються на сервері.
- Користувачі можуть виконувати базові операції над світлинами з використанням Cloudinary.
- Користувачі можуть створювати посилання на трансформоване зображення для перегляду світлини в вигляді URL та QR-code.

## Коментування

- Під кожною світлиною є блок з коментарями.
- Користувачі можуть коментувати світлини один одного.
- Користувач може редагувати свій коментар, але не видаляти.
- Адміністратори та модератори можуть видаляти коментарі.

## Технічні деталі

У цьому розділі можна додати технічні деталі, наприклад, як запустити проект, вимоги до середовища, інструкції зі збірки та розгортання, тощо.
