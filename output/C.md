تعرف إنك ينفع تضغط الويندوز بتاعك وتوفر في حوالي الـ 10 جيجا من الـ C؟
طب تعرف إنك ينفع تضغط أي ملف على جهازك وتوفر أحياناً إلى ما يقرب من 50% من المساحة؟

السلام عليكم، معاك أحمد طه من Creative Geek.
وأنا النهاردة مش جاي أقول جديد، أنا كتبت مقال قبل كدة بيوضحلك الـ File Compression وآلية عمله.
اللي جاي أقوله جديد هو طريقة أحسن بكتير لاستخدام الخاصية دي.

## مراجعة سريعة لضغط الملفات

بس للي مقراش المقال القديم، دي مراجعة سريعة تعرفك أنا بتكلم عن إيه:
نظام الملفات NTFS بيدعم خاصية بتخليك تضغط الملفات بكذا خوارزمية ضغط متاحة.
ده بيشتغل عن طريق تقليل حجم الملفات زي أي ضغط عادي جداً، بس الفكرة إنه بيتقري وهو مضغوط وبعد كدة البروسيسور يفك ضغطه في الرام.
وبالتالي إنت بتشتري مساحة على وحدة التخزين بتاعتك مقابل آداء البروسيسور.
الفرق في الآداء على أغلب الأجهزة بيتحسن أساساً، لإنك نادراً ما بتخلي البروسيسور يبقى 100%، لكن أغلب الوقت الهاردات بتاعتك بتكون مليانة أو بتكون محتاج تقرا منها ملفات كتيرة زي وانت مشغل لعبة مثلاً.

## ضغط الويندوز باستخدام compact.exe

ويندوز فيه برنامج صغير اسمه compact.exe، ده بيشغّل خاصية الضغط دي.
تقدر تضغط ويندوز عن طريقها باستخدام الأمر ده:
اقفل أي برنامج وافتح cmd as admin وحط الأمر ودوس انتر:

```
Compact.exe /CompactOS:always
```

هياخد شوية وقت، سيبه، هيفضيلك حوالي 10 جيجا (ممكن أقل وممكن أكتر).

## Compactor: حل أسهل وأذكى للضغط

المهم فيه واحد الله يكرمه كتبلنا برنامج أوبن سورس اسمه **Compactor** وظيفته يسهل إستخدام الأداة دي على أي ملف يعجبك ويستخدمها بذكاء أكبر.
كفايانا رغي عشان انت مبتحبش تقرا نظريات كتير.
ده لينك البرنامج على جيت هاب: [https://github.com/Freaky/Compactor](https://github.com/Freaky/Compactor)

هتفتحه (يستحسن as admin) وهتروح لقايمة الإعدادات.
اختار الـ Compression وخليه LZX عشان تضغط الملفات بأكبر قدر ممكن.
لو عندك بروسيسور قديم أو بطيئ اختار حاجة غيره، ممكن تخليك في الـ default لو محتار.
متنساش تدوس save.

هترجع من فوق لـ compact وتختار الفولدر من زرار Choose a folder.
بفرض إنك مضغطتش الفولدر ده قبل كدة هيجيلك 4 ألوان قدامك:

*   **الأبيض:** دي المساحة اللي انت وفرتها، وطبعاً لو الفولدر مش مضغوط هتكون صفر.
*   **الأخضر:** دي مساحة الملفات وهي مضغوطة، طبعاً في الأول هتكون صفر عشان مفيش ملفات مضغوطة
*   **الأزرق:** دي الملفات القابلة للضغط

وهنا تظهر ميزة حلوة للبرنامج ده، إنه عنده hash table بيقدر عن طريقه يعمل skip للملفات اللي هو عارف انها مضغوطة زي ملفات الريباك بتاعت الألعاب.

*   **الأصفر أو البرتقالى:** ودي الملفات اللي هو عارف إنها مش هتوفرلك مساحة فبيستثنيها من الضغط عشان يوفر وقتك.

طبعاً فيه ملفات كتير هو ميعرفش عنها حاجة وفيه ملفات هو أول مرة يشوفها فدول مش هيستثنيهم فممكن تقعد تضغط 60 جيجا وفي الآخر توفر ربع جيجا بس عادي.

## نصائح لإستخدام Compactor بكفاءة

لو انت فاهم دنيتك تقدر تسيب البوست خلاص.
أما للباقيين فهقولك تستخدم البرنامج ده كويس ازاي:

*   الأول متنساش تشغله as admin
*   لو معاك بروسيسور حلو وفارش معاك أرضية كويسة فهتشغل البرنامج على فولدرات الألعاب بتاعتك كلها، هيقلل وقت الـ Loading وهيضغط جامد في المساحة، هياخد وقت طبعاً فسيبه شغال بالليل.

### هيضغط قد ايه بالزبط؟

ده جدول فيه بتاع 5000 لعبة وحجمهم قبل وبعد الضغط: [link to be added]
ممكن ترجع للجدول وتشغل البرنامج على الألعاب اللي انت شايفها مستاهلة بس

### متستخدمهوش على الفولدرات دي:

*   ملفات الويندوز، هيتعملها skip تلقائي.
*   فولدر الـ AppData، ممكن تستخدمه عليه بس احتمال كبير يسجل خروجك من كتير من المواقع في المتصفح عشان الملفات اتعدلت بدون اذن (خطوة أمان وكدة).
*   الفولدرات اللي في الـ C بالجملة، يعني متروحش تشغله على Program Files مرة واحدة، بس شغله على برنامج برنامج باختيارك من جوا عادي.
*   الأفلام وملفات الفيديو والصور، هيتعملها إستثناء تلقائي عشان هي مضغوطة لوحدها.
*   ملفات الريباك والملفات المضغوطة، هيتعملها إستثناء برضه

### إستخدمه على الفولدرات دي:

*   ألعاب ستيم عادي
*   برامج أدوبي كلها بلا استثناء.
*   برامج الأوفيس.
*   برامج أوتوديسك بلا استثناء برضه.
*   برامج توباز.
*   البرامج اللي علي شاكلتهم، أي برنامج كبير جرب تضغطه، أهم حاجة متفتحهوش وهو بيتضغط.

## ملحوظات مهمة

*   المفروض البرنامج فيه خاصية File Locking عشان الملف ميحصلهوش حاجة لو الكهربا قطعت وانت بتضغط أو لو الملف كان مفتوح وهو بيتضغط بس دي حاجة مجربتهاش بنفسي.
*   الـ Progress bar بيحسب بعدد الملفات اللي هو خلصها، يعني ممكن لو بتضغط فولدر فيه 14 ملف صغيرين أقل من ميجا وملف واحد كبير حجمه 17 جيجا مثلاً هتلاقي الـ Progress جري بسرعة ووقف عند حتة معينة فترة طويلة جداً مقارنة بالباقيين، ده كدة شغال عادي مش مهنج (البرنامج مهنجش معايا ولا مرة للعلم) وعشان تتأكد إفتح تاسك مانجر وإتأكد إن فيه إستهلاك من السيستيم للبروسيسور والديسك
*   لو دوست Stop مش هيقف إلا لما يخلص الملف اللي في ايده حتى لو كان الملف ده كبيرهم، اوعي تعمله end task إلا لو مستغني عن ملفاتك
*   لو دوست كليك يمين على أي فولدر وروحت للـ Properties هتلاقي size دي المساحة الأصلية و size on disk دي المساحة بعد الضغط
*   لو أي ملف إتغير بعد الضغط هيتفك ضغطه، يعني اللعبة نزلها أبديت، فيه ملف جديد دخل الفولدر، أو نقلت الفولدر لهارد تاني، في الحالات دي كلها هيرجع مفكوك ولازم تضغطه تاني، دي حاجة كويسة عشان الضغط التلقائي ده كان أكبر عيب في الطريقة القديمة بتاعت ويندوز في ضغط الفولدرات، كان بيحتاج ضعف المساحة مكان فاضي عشان يعدل أي ملف، كذلك كان بيقلل الآداء بشكل بشع لإنه بيضغط الملفات تاني كل مرة تفتحها فيها وبيضغط أي ملف بيدخل الفولدر فدي كلها كوارث آداء.
*   الملفات المضغوطة بخوارزمية معينة مينفعش تعيد ضغطها بخوارزمية مختلفة، لازم تفكها الأول (البرنامج فيه فك ضغط) وبعدين تضغطها تاني.
*   الملفات المضغوطة عموماً بيتعملها skip تلقائي فمش هتوجع دماغك لو عايز تضغط نفس الفولدر كذا مرة بعد ما ضيفتله ملفين تلاتة

بعد ما تخلص المواضيع دي كلها كدة المفروض الـ C يفضالك منها حوالي نصها وممكن أكتر وفولدرات الجيمز هتلاقي بعض الألعاب خسّت كتير وبعضها فضل زي ما هو

ابقى ارجع بقى للمقال ده عشان تفضي شوية كمان من الـ C:
[link to be added]

ده اللي كان عندي انهاردة، أشوفكم مرة تانية والسلام عليكم