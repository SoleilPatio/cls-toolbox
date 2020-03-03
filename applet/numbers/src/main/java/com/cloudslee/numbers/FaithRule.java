package com.cloudslee.numbers;

public class FaithRule {

	static public CheckResult checkRule(int num) {
		final float step = 0.25f;

		CheckResult result = new CheckResult();
		DigitalApart dap = new DigitalApart();

		result.puregood = true;
		result.score = 0;
		dap.setNumber(num);

		/*
		 * Check "8s" / "4s" / ascent
		 */
		float acent_score = 0;
		boolean break_cont = false;
		for (int i = 1; i <= dap.magnitude(); i++) {
			/* 8s */
			if (dap.d(i) == 8) {
				result.score += step;
				result.commentaries.add(String.format("found 8. <%.2f>", step));
			}

			/* 4s */
			if (dap.d(i) == 4) {
				result.score -= step;
				result.commentaries.add(String.format("found 4. <%.2f>", -step));
				result.puregood = false;
			}

			/* Ascent */

			if (i < dap.magnitude() && !break_cont) {
				if (dap.d(i) > dap.d(i + 1)) {
					acent_score += step;
				} else if (dap.d(i) == dap.d(i + 1)) {
					acent_score += 0;
				} else {
					break_cont = true;
				}
			}
		}

		/* Ascent */
		if (acent_score > 0) {
			result.score += acent_score;
			result.commentaries.add(String.format("acent order<%.2f>", acent_score));
		}

		return result;
	}
}
