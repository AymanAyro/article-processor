فيه ميزة مفيدة جداً في أغلب أنظمة الملفات مفيش كتير يعرفوها اسمها **Symbolic Links**.

الخاصية دي بتعمل زي بورتال كدة يشاور على مكان ملف من مكان تاني، حاجة عاملة زي الـ Shortcut كدة بس بتشتغل مع البرامج والألعاب والويندوز بشكل عام.

أنا إستخدمت الخاصية دي عشان ألعب Starfield من غير stutters كل شوية، عشان حجمها كبير ومفيش مكان يكفيها في أي SSD واحد عندي... روحت قسّمت اللعبة على هاردين مختلفين واتنين SSD مختلفين.
يعني اللعبة كانت شغالة وبتـ load من 4 أجهزة تخزين مختلفة.

## يعني إيه Symbolic Links؟

فيه أمر في ويندوز اسمه `mklink` بيخليك تعمل اللينكات دي، متشيلش هم الأوامر هقولك على طريقة سهلة في الآخر.

فيه كذا نوع من اللينكات، أهمهم هما الـ **Symbolic link** والـ **Hard link**.

- الـ Symbolic link اسمه برضه soft link، بيشتغل في طبقة السوفتوير، بيعمل ملف يشاور على ملف تاني والملف التاني ده بيشاور على مكان الداتا الفيزيائي في الهارد.
- أما الـ Hard link فهو مدعوم من كل أنظمة التشغيل تقريباً (القديمة خصوصاً) ومدعوم في نظام ملفات Fat32، بيعمل ملف يشاور على مكان الداتا الفيزيائي مباشرةً.

## استخدامات الـ Symbolic Links:

- ممكن مثلاً لو عندك ملف كبير وفيه برنامجين مختلفين بيستخدموه تقوم عامل لينك منه للبرنامج التاني بدل ما تنسخ الملف وياخد مساحة زيادة.
- ممكن زي ما أنا عملت تاخد ملف من لعبة وتحطه في هارد تاني وتعمل لينك منه لمكان اللعبة الأصلي.
- ممكن مثلاً تنقل فولدر برنامج سطبته في الـ C لأي مكان تاني براحتك وترجع تعمل لينك للمكان الأصلي في الـ C، البرنامج ولا هياخد باله من حاجة وهيشتغل عادي.

## تنبيهات مهمة:

* السوفت لينك بيشتغل من الكيرنال، فمينفعش تستعمله مع أي لعبة فيها Anti-cheat
* متنقلش ملفات السيستيم، فولدر اليوزر، فولدر Downloads، ولا حتى فولدر temp، حصلت مشاكل كتيرة لما جربت كدة.
* جرب اللي عاوز تجربه على ملف ملهوش لازمة الأول (مثلاً هيحصل إيه لو مسحت اللينك؟ هل الملف هيتمسح؟ جرب وشوف) وبعدين جرب انقل برامجك وألعابك وملفاتك التقيلة.

## طريقة عمل Symbolic Links بسهولة:

1. سيرش عن برنامج: **Link Shell Extension (LSE)** وحمله وسطبه.
2. دوس كليك يمين على أي ملف أو فولدر عايز تعمله لينك.
3. اختار **Pick Link Source**.
4. روح للمكان اللي عايز تحط اللينك فيه (اعتبر نفسك بتلعب لعبة بورتال).
5. دوس كليك يمين في حتة فاضية واختار **Drop As** اختار **Symbolic link**.
6. استمتع؟ استفيد؟ انبسط؟ اعمل اللي تعمله.

* بكرر، جرب على ملف ملهوش لازمة الأول
* لأصحاب ويندوز 11، خيارات كليك يمين اللي أنا قولتها دي هتلاقيها في Show more options