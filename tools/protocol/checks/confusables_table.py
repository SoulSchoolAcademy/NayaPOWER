"""Confusable-character fold table for seat-identity comparison.

Provenance: Unicode confusables.txt, UTS #39, Version 18.0.0
(date 2026-08-06), fetched 2026-10-09.
https://www.unicode.org/Public/security/latest/confusables.txt

Derivation rule (class-first, not instance-first): keep every mapping
whose SOURCE is one non-ASCII character in Unicode categories L* / Nd /
Nl (letters and numbers) and whose TARGET is one ASCII alphanumeric
character. Fullwidth/halfwidth ("Width") sources are INCLUDED -- NFKC
folds most of them, but the table carries them anyway so the fold step
is explicit and order-independent (see the NFKC-consistency rule below).

Result: 1453 single-character confusables across Latin, Cyrillic,
Greek, Armenian and other scripts, each mapping to its canonical ASCII
letter/digit, PLUS 2 NFKC-closure entries: U+03F2/U+03F9 (Greek lunate
sigmas, enumerated -> 'c') are NFKC-mapped to U+03C2/U+03A3 (final
sigma / capital sigma) before any confusable fold sees them, so the
closure adds U+03C2 -> 'c' and U+03A3 -> 'c'. An attacker can type the
NFKC outputs directly, and the enumerated pair alone does not cover
them.

PLUS 30 NFKC-retargeted entries (2026-10-09): for every enumerated pair
(s -> t) where NFKC(s) is a single ASCII character u with fold(u) != t,
the target is retargeted to the NFKC behavior. NFKC's compatibility
decomposition is the character's canonical identity; confusables.txt's
MA visual mapping is defeated by the pipeline's own NFKC step, and
leaving the MA target made the two fold orders disagree on the same
character (batch-3's fold-first fixpoint honored the table, batch-4's
NFKC-first lane honored NFKC). The 30: 14 stylistic digit forms
(fullwidth / mathematical / segmented 0 and 1) -> '0' / '1' (digits
stay digits -- the digit/letter non-fold policy, now in BOTH lanes),
U+017F LATIN SMALL LETTER LONG S -> 's' (not confusables.txt's 'f'),
15 I-variants (U+2110 SCRIPT CAPITAL I, U+2111 BLACK-LETTER CAPITAL I,
U+2160 ROMAN NUMERAL ONE, U+FF29 FULLWIDTH LATIN CAPITAL LETTER I
and 11 mathematical capital-I forms) -> 'i' (not confusables.txt's
'l'). A human reading "\u017fin-1" reads "sin-1", not "fin-1"; the
table now agrees with the reader.

Total: 1455. The table is NFKC-CONSISTENT: for every source s,
NFKC-first-fold(s) == table target, so fold ORDER is irrelevant --
fold_to_ascii_fixpoint (NFKC-after-fold, iterated) and a single
NFKC-first pass produce the same fold on every input. The two protocol
lanes (merge_authority._seat_key, falsification_first._skeleton) share
this one book byte-identically and cannot diverge on the fold step.

The fold is applied to FIXPOINT as NFKC(confusable-fold(x)) by the
batch-3 lane, because neither order alone closed the class on the
pre-retarget table (measured 2026-10-09):
  - NFKC-first leaves 32 enumerated entries dead: NFKC maps them to
    forms the table never sees -- e.g. U+03F2 -> U+03C2, U+017F ->
    's', U+2110 -> 'I' -- and the strip then deletes or mis-folds
    them ("\u03f2oda-1" folded to "oda1", passing as a different seat).
  - Fold-first alone misses 45 measured characters whose NFKC output
    IS a table source -- e.g. U+02E0 MODIFIER LETTER SMALL GAMMA ->
    U+0263, a table source -> 'y' -- which a single pass never folds.
The fixpoint over the NFKC-after-fold composition closes both lanes.
It converges in at most 3 passes: each pass maps every table source
to ASCII, and NFKC is idempotent, so no input can oscillate.
Re-applying the confusable fold alone (without NFKC in the loop)
fixes nothing -- measured 0 of 32 -- because the dead entries'
NFKC outputs are not table sources.

Regeneration: run the derivation script saved at
~/workspace/batch3-confusables-evidence/ (confusables.txt +
confusables-derived-table.json) and re-emit these two strings, then
(1) re-apply the NFKC-closure rule (for every enumerated pair (s -> t)
with NFKC(s) = u a single non-ASCII char not already a source, add
u -> t), (2) re-apply the NFKC-retarget rule (for every pair (s -> t)
with NFKC(s) = u a single ASCII char and fold(u) != t, set s -> fold(u)),
and re-verify: the closure property (for every source s,
fold_to_ascii_fixpoint(s) == its target) AND NFKC-consistency (for every
source s, NFKC-first-fold(s) == its target).
"""

import unicodedata

_SRC = "\u01a7\u03e8\u10c7\u14bf\u1616\u1cb7\ua644\ua6ef\ua75a\uff12\U0001d7d0\U0001d7da\U0001d7e4\U0001d7ee\U0001d7f8\U0001fbf2\u01b7\u021c\u0417\u04e0\u0545\u0969\u0ae9\u1702\u1c95\u2c9c\u2cc4\u2ccc\ua76a\ua7ab\uff13\U000118ca\U00016f3b\U0001d7d1\U0001d7db\U0001d7e5\U0001d7ef\U0001d7f9\U0001fbf3\u13ce\uab9e\uff14\U000118af\U0001d7d2\U0001d7dc\U0001d7e6\U0001d7f0\U0001d7fa\U0001fbf4\u01bc\uff15\U000118bb\U0001d7d3\U0001d7dd\U0001d7e7\U0001d7f1\U0001d7fb\U0001fbf5\u03ec\u0431\u13ee\u2cd2\u2cd3\u2cdc\ua543\uabbe\uff16\U000118d5\U0001d7d4\U0001d7de\U0001d7e8\U0001d7f2\U0001d7fc\U0001fbf6\u172a\u1c84\uff17\U000104d2\U000118c6\U0001d7d5\U0001d7df\U0001d7e9\U0001d7f3\U0001d7fd\U0001fbf7\u0222\u0223\u09ea\u0a6a\ua589\uff18\U0001031a\U000169fe\U0001d7d6\U0001d7e0\U0001d7ea\U0001d7f4\U0001d7fe\U0001fbf8\u09ed\u0a67\u0b68\u0d6d\u2cca\u2ccb\ua76e\ua76f\uff19\U000118ac\U000118cc\U000118d6\U000169c1\U0001d7d7\U0001d7e1\U0001d7eb\U0001d7f5\U0001d7ff\U0001e2f2\U0001fbf9\u0251\u0391\u03b1\u0410\u0430\u13aa\u15c5\ua4ee\uab64\uff21\uff41\U000102a0\U00016f40\U0001d400\U0001d41a\U0001d434\U0001d44e\U0001d468\U0001d482\U0001d49c\U0001d4b6\U0001d4d0\U0001d4ea\U0001d504\U0001d51e\U0001d538\U0001d552\U0001d56c\U0001d586\U0001d5a0\U0001d5ba\U0001d5d4\U0001d5ee\U0001d608\U0001d622\U0001d63c\U0001d656\U0001d670\U0001d68a\U0001d6a8\U0001d6c2\U0001d6e2\U0001d6fc\U0001d71c\U0001d736\U0001d756\U0001d770\U0001d790\U0001d7aa\u0184\u0392\u0412\u042c\u07d5\u13cf\u13f4\u1472\u15af\u15f7\u212c\u2c82\ua4d0\ua557\ua7b4\uff22\uff42\U00010282\U000102a1\U00010301\U0001031c\U0001d401\U0001d41b\U0001d435\U0001d44f\U0001d469\U0001d483\U0001d4b7\U0001d4d1\U0001d4eb\U0001d505\U0001d51f\U0001d539\U0001d553\U0001d56d\U0001d587\U0001d5a1\U0001d5bb\U0001d5d5\U0001d5ef\U0001d609\U0001d623\U0001d63d\U0001d657\U0001d671\U0001d68b\U0001d6a9\U0001d6e3\U0001d71d\U0001d757\U0001d791\u03f2\u03f9\u03c2\u03a3\u0421\u0441\u1004\u105a\u13df\u1c83\u1d04\u2102\u212d\u216d\u217d\u2ca4\u2ca5\ua4da\uabaf\uff23\uff43\U000102a2\U00010302\U00010415\U0001043d\U0001051b\U000118e9\U0001d402\U0001d41c\U0001d436\U0001d450\U0001d46a\U0001d484\U0001d49e\U0001d4b8\U0001d4d2\U0001d4ec\U0001d520\U0001d554\U0001d56e\U0001d588\U0001d5a2\U0001d5bc\U0001d5d6\U0001d5f0\U0001d60a\U0001d624\U0001d63e\U0001d658\U0001d672\U0001d68c\u0501\u13a0\u13e7\u146f\u15de\u15ea\u2145\u2146\u216e\u217e\ua4d2\ua4d3\uff24\uff44\U0001d403\U0001d41d\U0001d437\U0001d451\U0001d46b\U0001d485\U0001d49f\U0001d4b9\U0001d4d3\U0001d4ed\U0001d507\U0001d521\U0001d53b\U0001d555\U0001d56f\U0001d589\U0001d5a3\U0001d5bd\U0001d5d7\U0001d5f1\U0001d60b\U0001d625\U0001d63f\U0001d659\U0001d673\U0001d68d\u0395\u0415\u0435\u04bd\u13ac\u212f\u2130\u2147\u2d39\ua4f0\ua5cb\uab32\uff25\uff45\U00010286\U000118a6\U000118ae\U0001d404\U0001d41e\U0001d438\U0001d452\U0001d46c\U0001d486\U0001d4d4\U0001d4ee\U0001d508\U0001d522\U0001d53c\U0001d556\U0001d570\U0001d58a\U0001d5a4\U0001d5be\U0001d5d8\U0001d5f2\U0001d60c\U0001d626\U0001d640\U0001d65a\U0001d674\U0001d68e\U0001d6ac\U0001d6e6\U0001d720\U0001d75a\U0001d794\u017f\u0192\u0284\u03dc\u0584\u07d3\u15b4\u1e9d\u2131\ua4dd\ua798\ua799\uab35\uff26\uff46\U00010287\U000102a5\U00010525\U000118a2\U000118c2\U0001d405\U0001d41f\U0001d439\U0001d453\U0001d46d\U0001d487\U0001d4bb\U0001d4d5\U0001d4ef\U0001d509\U0001d523\U0001d53d\U0001d557\U0001d571\U0001d58b\U0001d5a5\U0001d5bf\U0001d5d9\U0001d5f3\U0001d60d\U0001d627\U0001d641\U0001d65b\U0001d675\U0001d68f\U0001d7ca\u018d\u0261\u050c\u0581\u13c0\u13f3\u1d83\u210a\ua4d6\uff27\uff47\U0001d406\U0001d420\U0001d43a\U0001d454\U0001d46e\U0001d488\U0001d4a2\U0001d4d6\U0001d4f0\U0001d50a\U0001d524\U0001d53e\U0001d558\U0001d572\U0001d58c\U0001d5a6\U0001d5c0\U0001d5da\U0001d5f4\U0001d60e\U0001d628\U0001d642\U0001d65c\U0001d676\U0001d690\u0397\u041d\u04ba\u04bb\u0570\u10b9\u13bb\u13c2\u157c\u210b\u210c\u210d\u210e\u2c8e\ua4e7\uff28\uff48\U000102cf\U0001d407\U0001d421\U0001d43b\U0001d46f\U0001d489\U0001d4bd\U0001d4d7\U0001d4f1\U0001d525\U0001d559\U0001d573\U0001d58d\U0001d5a7\U0001d5c1\U0001d5db\U0001d5f5\U0001d60f\U0001d629\U0001d643\U0001d65d\U0001d677\U0001d691\U0001d6ae\U0001d6e8\U0001d722\U0001d75c\U0001d796\u0131\u0269\u026a\u03b9\u0456\u0582\u13a5\u2139\u2148\u2170\u2c93\ua647\uab75\uff49\U000118c3\U0001d422\U0001d456\U0001d48a\U0001d4be\U0001d4f2\U0001d526\U0001d55a\U0001d58e\U0001d5c2\U0001d5f6\U0001d62a\U0001d65e\U0001d692\U0001d6a4\U0001d6ca\U0001d704\U0001d73e\U0001d778\U0001d7b2\u0237\u037f\u03f3\u0408\u0458\u0575\u13ab\u148d\u2149\ua4d9\ua7b2\uff2a\uff4a\U0001d409\U0001d423\U0001d43d\U0001d457\U0001d471\U0001d48b\U0001d4a5\U0001d4bf\U0001d4d9\U0001d4f3\U0001d50d\U0001d527\U0001d541\U0001d55b\U0001d575\U0001d58f\U0001d5a9\U0001d5c3\U0001d5dd\U0001d5f7\U0001d611\U0001d62b\U0001d645\U0001d65f\U0001d679\U0001d693\U0001d6a5\u039a\u041a\u13e6\u16d5\u2c94\ua4d7\uff2b\uff4b\U00010518\U0001d40a\U0001d424\U0001d43e\U0001d458\U0001d472\U0001d48c\U0001d4a6\U0001d4c0\U0001d4da\U0001d4f4\U0001d50e\U0001d528\U0001d542\U0001d55c\U0001d576\U0001d590\U0001d5aa\U0001d5c4\U0001d5de\U0001d5f8\U0001d612\U0001d62c\U0001d646\U0001d660\U0001d67a\U0001d694\U0001d6b1\U0001d6eb\U0001d725\U0001d75f\U0001d799\u0196\u01c0\u0399\u0406\u04c0\u04cf\u05d5\u05df\u0627\u0661\u06f1\u07ca\u13de\u14aa\u16c1\u16d0\u2110\u2111\u2112\u2113\u2160\u216c\u217c\u2c92\u2cd0\u2d4a\u2d4f\ua4e1\ua4f2\ua56f\ua781\ua7ae\ua7fe\ufe8d\ufe8e\uff11\uff29\uff2c\uff4c\U0001028a\U00010309\U0001041b\U0001050e\U00010526\U00010926\U00010c3e\U00010ca5\U000118a3\U000118b2\U00016f16\U00016f28\U0001d408\U0001d40b\U0001d425\U0001d43c\U0001d43f\U0001d459\U0001d470\U0001d473\U0001d48d\U0001d4c1\U0001d4d8\U0001d4db\U0001d4f5\U0001d50f\U0001d529\U0001d540\U0001d543\U0001d55d\U0001d574\U0001d577\U0001d591\U0001d5a8\U0001d5ab\U0001d5c5\U0001d5dc\U0001d5df\U0001d5f9\U0001d610\U0001d613\U0001d62d\U0001d644\U0001d647\U0001d661\U0001d678\U0001d67b\U0001d695\U0001d6b0\U0001d6ea\U0001d724\U0001d75e\U0001d798\U0001d7cf\U0001d7d9\U0001d7e3\U0001d7ed\U0001d7f7\U0001e141\U0001ee00\U0001ee80\U0001fbf1\u039c\u03fa\u041c\u13b7\u15f0\u16d6\u2133\u216f\u2c98\ua4df\uff2d\U000102b0\U00010311\U00010c21\U0001d40c\U0001d440\U0001d474\U0001d4dc\U0001d510\U0001d544\U0001d578\U0001d5ac\U0001d5e0\U0001d614\U0001d648\U0001d67c\U0001d6b3\U0001d6ed\U0001d727\U0001d761\U0001d79b\u039d\u0578\u057c\u2115\u2c9a\ua4e0\uff2e\uff4e\U00010513\U00011abe\U0001d40d\U0001d427\U0001d441\U0001d45b\U0001d475\U0001d48f\U0001d4a9\U0001d4c3\U0001d4dd\U0001d4f7\U0001d511\U0001d52b\U0001d55f\U0001d579\U0001d593\U0001d5ad\U0001d5c7\U0001d5e1\U0001d5fb\U0001d615\U0001d62f\U0001d649\U0001d663\U0001d67d\U0001d697\U0001d6b4\U0001d6ee\U0001d728\U0001d762\U0001d79c\u039f\u03bf\u03c3\u03ed\u041e\u043e\u0555\u0585\u05e1\u0647\u0665\u06be\u06c1\u06d5\u06f5\u07c0\u07cb\u0840\u0966\u09e6\u0a66\u0ae6\u0b20\u0b66\u0be6\u0c66\u0ce6\u0d20\u0d66\u0e50\u0ed0\u101d\u1040\u10ff\u110b\u11bc\u12d0\u17e0\u1a45\u1a80\u1a90\u1c82\u1cbf\u1d0f\u1d11\u2134\u2c9e\u2c9f\u2d54\u3007\u3147\ua4f3\uab3d\ufba6\ufba7\ufba8\ufba9\ufbaa\ufbab\ufbac\ufbad\ufee9\ufeea\ufeeb\ufeec\uff10\uff2f\uff4f\uffb7\U00010292\U000102ab\U0001030f\U00010404\U0001042c\U000104c2\U000104ea\U00010516\U0001092c\U00010c17\U00010d07\U00011124\U000114d0\U000118b5\U000118c8\U000118d7\U000118e0\U00016ae9\U0001d40e\U0001d428\U0001d442\U0001d45c\U0001d476\U0001d490\U0001d4aa\U0001d4de\U0001d4f8\U0001d512\U0001d52c\U0001d546\U0001d560\U0001d57a\U0001d594\U0001d5ae\U0001d5c8\U0001d5e2\U0001d5fc\U0001d616\U0001d630\U0001d64a\U0001d664\U0001d67e\U0001d698\U0001d6b6\U0001d6d0\U0001d6d4\U0001d6f0\U0001d70a\U0001d70e\U0001d72a\U0001d744\U0001d748\U0001d764\U0001d77e\U0001d782\U0001d79e\U0001d7b8\U0001d7bc\U0001d7ce\U0001d7d8\U0001d7e2\U0001d7ec\U0001d7f6\U0001e140\U0001e2f0\U0001ee24\U0001ee84\U0001fbf0\xfe\u01bf\u03a1\u03c1\u03f1\u03f8\u0420\u0440\u13e2\u146d\u2119\u2ca2\u2ca3\u2cce\u2ccf\ua4d1\uff30\uff50\U00010295\U0001d40f\U0001d429\U0001d443\U0001d45d\U0001d477\U0001d491\U0001d4ab\U0001d4c5\U0001d4df\U0001d4f9\U0001d513\U0001d52d\U0001d561\U0001d57b\U0001d595\U0001d5af\U0001d5c9\U0001d5e3\U0001d5fd\U0001d617\U0001d631\U0001d64b\U0001d665\U0001d67f\U0001d699\U0001d6b8\U0001d6d2\U0001d6e0\U0001d6f2\U0001d70c\U0001d71a\U0001d72c\U0001d746\U0001d754\U0001d766\U0001d780\U0001d78e\U0001d7a0\U0001d7ba\U0001d7c8\u051a\u051b\u0563\u0566\u211a\u2d55\uff31\uff51\U0001d410\U0001d42a\U0001d444\U0001d45e\U0001d478\U0001d492\U0001d4ac\U0001d4c6\U0001d4e0\U0001d4fa\U0001d514\U0001d52e\U0001d562\U0001d57c\U0001d596\U0001d5b0\U0001d5ca\U0001d5e4\U0001d5fe\U0001d618\U0001d632\U0001d64c\U0001d666\U0001d680\U0001d69a\u01a6\u024c\u0433\u13a1\u13d2\u1587\u1d26\u211b\u211c\u211d\u2c85\ua4e3\uab47\uab48\uab81\uff32\uff52\U000104b4\U00016a19\U00016f35\U0001d411\U0001d42b\U0001d445\U0001d45f\U0001d479\U0001d493\U0001d4c7\U0001d4e1\U0001d4fb\U0001d52f\U0001d563\U0001d57d\U0001d597\U0001d5b1\U0001d5cb\U0001d5e5\U0001d5ff\U0001d619\U0001d633\U0001d64d\U0001d667\U0001d681\U0001d69b\u01bd\u0405\u0455\u054f\u0d1f\u10bd\u10fd\u13d5\u13da\u1cbd\ua4e2\ua576\ua731\uabaa\uff33\uff53\U00010296\U00010420\U00010448\U000118c1\U00016ad6\U00016f3a\U0001d412\U0001d42c\U0001d446\U0001d460\U0001d47a\U0001d494\U0001d4ae\U0001d4c8\U0001d4e2\U0001d4fc\U0001d516\U0001d530\U0001d54a\U0001d564\U0001d57e\U0001d598\U0001d5b2\U0001d5cc\U0001d5e6\U0001d600\U0001d61a\U0001d634\U0001d64e\U0001d668\U0001d682\U0001d69c\u03a4\u0422\u07e0\u13a2\u2ca6\u3112\u4e05\ua4d4\ua50b\uff34\uff54\U00010297\U000102b1\U00010315\U000118bc\U00016f0a\U0001d413\U0001d42d\U0001d447\U0001d461\U0001d47b\U0001d495\U0001d4af\U0001d4c9\U0001d4e3\U0001d4fd\U0001d517\U0001d531\U0001d54b\U0001d565\U0001d57f\U0001d599\U0001d5b3\U0001d5cd\U0001d5e7\U0001d601\U0001d61b\U0001d635\U0001d64f\U0001d669\U0001d683\U0001d69d\U0001d6bb\U0001d6f5\U0001d72f\U0001d769\U0001d7a3\u028b\u03c5\u054d\u057d\u1200\u144c\u1d1c\ua4f4\ua79f\uab4e\uab52\uff35\uff55\U000104ce\U000104f6\U000118b8\U000118d8\U00016f42\U0001d414\U0001d42e\U0001d448\U0001d462\U0001d47c\U0001d496\U0001d4b0\U0001d4ca\U0001d4e4\U0001d4fe\U0001d518\U0001d532\U0001d54c\U0001d566\U0001d580\U0001d59a\U0001d5b4\U0001d5ce\U0001d5e8\U0001d602\U0001d61c\U0001d636\U0001d650\U0001d66a\U0001d684\U0001d69e\U0001d6d6\U0001d710\U0001d74a\U0001d784\U0001d7be\u03bd\u0474\u0475\u05d8\u0667\u06f7\u13d9\u142f\u1d20\u2164\u2174\u2d38\ua4e6\ua6df\uaba9\uff36\uff56\U0001051d\U00010c1f\U00011706\U000118a0\U000118c0\U00016f08\U0001d415\U0001d42f\U0001d449\U0001d463\U0001d47d\U0001d497\U0001d4b1\U0001d4cb\U0001d4e5\U0001d4ff\U0001d519\U0001d533\U0001d54d\U0001d567\U0001d581\U0001d59b\U0001d5b5\U0001d5cf\U0001d5e9\U0001d603\U0001d61d\U0001d637\U0001d651\U0001d66b\U0001d685\U0001d69f\U0001d6ce\U0001d708\U0001d742\U0001d77c\U0001d7b6\U0001e145\u026f\u0448\u0461\u051c\u051d\u0561\u13b3\u13d4\u1d21\u2cbd\ua4ea\ua7fa\uab83\uaba4\uff37\uff57\U0001170a\U0001170e\U0001170f\U000118e6\U0001d416\U0001d430\U0001d44a\U0001d464\U0001d47e\U0001d498\U0001d4b2\U0001d4cc\U0001d4e6\U0001d500\U0001d51a\U0001d534\U0001d54e\U0001d568\U0001d582\U0001d59c\U0001d5b6\U0001d5d0\U0001d5ea\U0001d604\U0001d61e\U0001d638\U0001d652\U0001d66c\U0001d686\U0001d6a0\u03a7\u0425\u0445\u1541\u157d\u16b7\u1763\u1cf5\u2169\u2179\u2cac\u2d5d\ua4eb\ua7b3\uff38\uff58\U00010290\U000102b4\U00010317\U00010527\U00010c13\U00010c82\U00010cc2\U0001d417\U0001d431\U0001d44b\U0001d465\U0001d47f\U0001d499\U0001d4b3\U0001d4cd\U0001d4e7\U0001d501\U0001d51b\U0001d535\U0001d54f\U0001d569\U0001d583\U0001d59d\U0001d5b7\U0001d5d1\U0001d5eb\U0001d605\U0001d61f\U0001d639\U0001d653\U0001d66d\U0001d687\U0001d6a1\U0001d6be\U0001d6f8\U0001d732\U0001d76c\U0001d7a6\u0263\u028f\u03a5\u03b3\u03d2\u0423\u0443\u04ae\u04af\u07cc\u10e7\u13a9\u13bd\u1d8c\u1eff\u213d\u2ca8\u2ca9\u311a\u4e2b\ua4ec\uab5a\uff39\uff59\U000102b2\U00010c20\U000118a4\U000118c4\U000118dc\U00016f43\U0001d418\U0001d432\U0001d44c\U0001d466\U0001d480\U0001d49a\U0001d4b4\U0001d4ce\U0001d4e8\U0001d502\U0001d51c\U0001d536\U0001d550\U0001d56a\U0001d584\U0001d59e\U0001d5b8\U0001d5d2\U0001d5ec\U0001d606\U0001d620\U0001d63a\U0001d654\U0001d66e\U0001d688\U0001d6a2\U0001d6bc\U0001d6c4\U0001d6f6\U0001d6fe\U0001d730\U0001d738\U0001d76a\U0001d772\U0001d7a4\U0001d7ac\u0396\u10cd\u13c3\u1d22\u2124\u2128\u2c6b\u2c6c\u2c8c\u2c8d\u2d2d\ua4dc\ua6c9\uab93\uff3a\uff5a\U00010507\U000118a9\U000118e5\U00011abc\U0001d419\U0001d433\U0001d44d\U0001d467\U0001d481\U0001d49b\U0001d4b5\U0001d4cf\U0001d4e9\U0001d503\U0001d537\U0001d56b\U0001d585\U0001d59f\U0001d5b9\U0001d5d3\U0001d5ed\U0001d607\U0001d621\U0001d63b\U0001d655\U0001d66f\U0001d689\U0001d6a3\U0001d6ad\U0001d6e7\U0001d721\U0001d75b\U0001d795"
_DST = "22222222222222223333333333333333333333344444444445555555556666666666666666777777777778888888888888899999999999999999999aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccccccccccccccccccccccccddddddddddddddddddddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesfffffffffffffffffffffffffffffffffffffffffffffgggggggggggggggggggggggggggggggggggghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiijjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkklllllllllllllllliillillllllllllllll1illllllllllllllillillilllillllillillillillillillilllllll11111lll1mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo00000oooo0pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrsssssssssssssssssssssssssssssssssssssssssssssssstttttttttttttttttttttttttttttttttttttttttttttttuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"


assert len(_SRC) == len(_DST) == 1455, "confusables table corrupted"
assert len(set(_SRC)) == len(_SRC), "duplicate confusable source in table"

#: str.translate map: every confusable -> its canonical ASCII character.
FOLD = str.maketrans(_SRC, _DST)


def fold_to_ascii_fixpoint(text: str) -> str:
    """Fold text toward canonical ASCII: iterate NFKC(confusable-fold(x))
    to fixpoint.

    One pass is not enough in either order on the pre-retarget table (see
    the module docstring: 32 enumerated entries die under NFKC-first, 45
    measured characters are missed under fold-first). The composition
    NFKC-after-fold is idempotent after at most 3 passes -- each pass maps
    every table source to ASCII and NFKC itself cannot oscillate -- so the
    loop always terminates; the 10-pass cap is a guard, not logic.
    On the NFKC-consistent table a single NFKC-first pass gives the same
    result; the fixpoint is kept because it is order-agnostic by
    construction.
    """
    cur = text
    for _ in range(10):
        nxt = unicodedata.normalize("NFKC", cur.translate(FOLD))
        if nxt == cur:
            return cur
        cur = nxt
    return cur
