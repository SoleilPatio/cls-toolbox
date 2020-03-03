package com.cloudslee.numbers;

import java.util.ArrayList;
import java.util.List;

public class CheckResult {

	public boolean puregood; // Pure good result
	public float score;
	public List<String> commentaries = new ArrayList<String>();

	public CheckResult merge(CheckResult result) {
		puregood = puregood & result.puregood;
		score += result.score;
		commentaries.addAll(result.commentaries);
		return this;
	}

	public CheckResult clear() {
		puregood = false;
		score = 0.0f;
		commentaries.clear();
		return this;
	}

	@Override
	public String toString() {
		String result = new String();

		result = String.format("score=%.2f\n", score);

		for (String str : commentaries) {
			result += str + "\n";
		}

		return result;
	}

}
