package com.cloudslee.numbers;

/**
 * 
 * @author clouds 奇門遁甲八門吉凶
 */
public class EightDoor {
	static private class Rule {
		int index;
		String name;
		String commentary;
		@SuppressWarnings("unused")
		boolean goodorbad;
		float score;

		public Rule(int idx, String nm, String comm, boolean gob, float sc) {
			index = idx;
			name = nm;
			commentary = comm;
			goodorbad = gob;
			score = sc;

		}
	}

	static private Rule[] record = {

			new Rule(1, "休門", "求財、婚姻嫁娶、遠行、新官上任等諸事皆宜。 休門的氣比較輕鬆，故很適合出外旅遊或非正式的商業 活動。", true, 1.0f),
			new Rule(2, "生門", "謀財、求職、作生意、遠行、婚姻嫁取等諸事皆宜。生門有生生不息的意思，故最適合求財作生意或有病求醫", true, 1.0f),
			new Rule(3, "傷門", "傷門意為破壞的磁場，若強出傷門易見血光，故一般吉事皆不宜。但很適合釣魚打獵、博戲、索債或圍捕盜賊，利刑事訴訟。", false, -1.0f),
			new Rule(4, "杜門", "杜門有隱藏的意思，適合隱身藏形躲災避難，其餘諸事皆不宜。若要躲起來不讓人發現杜門最適合。", false, -1.0f),
			new Rule(5, "景門", "景門是八門之中除開休生三門之外另一吉門。景門最利考試、廣告宣傳活動、遠行婚姻嫁娶等皆宜。", true, 1.0f),
			new Rule(6, "死門", "死門最凶，除弔喪捕獵之外其餘諸事不宜。", false, -2.0f),
			new Rule(7, "驚門", "驚門有驚恐怪異之意思，若強出此門易遇驚慌恐亂之事，利民事訴訟。", false, -1.0f),
			new Rule(8, "開門", "宜遠行，利求職新官上任、求財、婚姻嫁娶、訪友、見貴人。 不宜政治陰私之事，易被他人窺見。", true, 1.0f),

	};

	static public CheckResult checkRule(int num) {
		CheckResult result = new CheckResult();
		DigitalApart dap = new DigitalApart();

		dap.setNumber(num);

		int digitalsum = 0;
		for (int i = 1; i <= dap.magnitude(); i++) {
			digitalsum += dap.d(i);
		}

		int mod = digitalsum - (digitalsum / 8) * 8;

		if (mod == 0)
			mod = 8;

		int index = mod - 1;

		if (result.score > 0)
			result.puregood = true;
		else
			result.puregood = false;

		result.score = record[index].score;
		result.commentaries.add(String.format("%d:%s:%s<%.2f>", record[index].index, record[index].name,
				record[index].commentary, record[index].score));

		return result;

	}

}
