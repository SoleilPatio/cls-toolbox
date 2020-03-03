package com.cloudslee.numbers;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * 
 * @author clouds 81吉凶表
 */
public class EightyOneGoodOrIll {

	static private class Rule {
		int index;
		String commentary;
		String goodorbad;
		float score;

		public Rule(int idx, String comm, String gob, float sc) {
			index = idx;
			commentary = comm;
			goodorbad = gob;
			score = sc;

		}
	}

	static private Rule[] record = {
			new Rule(1, "繁榮發達，信用得固，萬人仰望，可獲成功。", "吉", 1.0f),
			new Rule(2, "動搖不安，一榮一枯，一盛一衰，勞而無功。", "凶", -1.0f),
			new Rule(3, "立身出世，有貴人助，天賜吉祥，四海名揚。", "吉", 1.0f),
			new Rule(4, "日被雲遮，苦難折磨，非有毅力，難望成功。", "凶", -1.0f),
			new Rule(5, "陰陽和合，精神愉快，榮譽達利，一門興隆。", "吉", 1.0f),
			new Rule(6, "萬寶集門，天降幸運，立志奮發，得成大功。", "吉", 1.0f),
			new Rule(7, "精力旺盛，頭腦明敏，排除萬難，必獲成功。", "吉", 1.0f),
			new Rule(8, "努力發達，貫徹志望，不忘進退，可期成功。", "吉", 1.0f),
			new Rule(9, "雖抱奇才，有才無命，獨營無力，財利難望。", "凶", -1.0f),
			new Rule(10, "烏雲遮月，暗淡無光，空費心力，徒勞無功。", "凶", -1.0f),
			new Rule(11, "草木逢春，枝葉沾露，穩建著實，必得人望。", "吉", 1.0f),
			new Rule(12, "薄弱無力，孤立無援，外祥內苦，謀事難成。", "凶", -1.0f),
			new Rule(13, "天賦吉運，能得人望，善用智慧，必獲成功。", "吉", 1.0f),
			new Rule(14, "忍得苦難，必有後福，是成是敗，惟靠堅毅。", "凶", -1.0f),
			new Rule(15, "謙恭做事，外得人和，大事成就，一門興隆。", "吉", 1.0f),
			new Rule(16, "能獲眾望，成就大業，名利雙收，盟主四方。", "吉", 1.0f),
			new Rule(17, "排除萬難，有貴人助，把握時機，可得成功。", "吉", 1.0f),
			new Rule(18, "經商做事，順利昌隆，如能慎始，百事亨通。", "吉", 1.0f),
			new Rule(19, "成功雖早，慎防虧空，內外不和，障礙重重。", "凶", -1.0f),
			new Rule(20, "智高志大，歷盡?難，焦心憂勞，進退兩難。", "凶", -1.0f),
			new Rule(21, "先歷困苦，後得幸福，霜雪梅花，春來怒放。", "吉", 1.0f),
			new Rule(22, "秋草逢霜，懷才不遇，憂愁怨苦，事不如意。", "凶", -1.0f),
			new Rule(23, "旭日昇天，名顯四方，漸次進展，終成大業。", "吉", 1.0f),
			new Rule(24, "錦繡前程，須靠自力，多用智謀，能奏大功。", "吉", 1.0f),
			new Rule(25, "天時地利，只久人和，講信修睦，即可成功。", "吉", 1.0f),
			new Rule(26, "波瀾起伏，千變萬化，凌駕萬難，必可成功。", "凶帶吉", -0.75f),
			new Rule(27, "一成一敗，一盛一衰，惟靠謹慎，可守成功。", "吉帶凶", -0.5f),
			new Rule(28, "魚臨旱地，難逃惡運，此數大凶，不如更名。", "凶", -1.0f),
			new Rule(29, "如龍得雲，青雲直上，智謀奮進，才略奏功。", "吉", 1.0f),
			new Rule(30, "吉凶參半，得失相伴，投機取巧，如賭一樣。", "吉帶凶", -0.5f),
			new Rule(31, "此數大吉，名利雙收，漸進向上，大業成就。", "吉", 1.0f),
			new Rule(32, "池中之龍，風雲際會，一躍上天，成功可望。", "吉", 1.0f),
			new Rule(33, "意氣用事，人和必失，如能慎始，必可昌隆。", "吉", 1.0f),
			new Rule(34, "災難不絕，難望成功，此數大凶，不如更名。", "凶", -1.0f),
			new Rule(35, "處事嚴謹，進退保守，學智兼具，成就非凡。", "吉", 1.0f),
			new Rule(36, "波瀾重疊，常陷窮困，動不如靜，有才無命。", "凶", -1.0f),
			new Rule(37, "逢凶化吉，吉人天相，以德取眾，必成大功。", "吉", 1.0f),
			new Rule(38, "名雖可得，利則難獲，藝界發展，可望成功。", "凶帶吉", -0.75f),
			new Rule(39, "雲?見月，雖有勞碌，光明坦途，指日可期。", "吉", 1.0f),
			new Rule(40, "一盛一衰，浮沉不定，知難而退，自獲天佑。", "吉帶凶", -0.5f),
			new Rule(41, "天賦吉運，德望兼備，繼續努力，前途無限。", "吉", 1.0f),
			new Rule(42, "事業不專，十九不成，專心進取，可望成功。", "吉帶凶", -0.5f),
			new Rule(43, "兩夜之花，外祥內苦，忍耐自重，轉凶為吉。", "吉帶凶", -0.5f),
			new Rule(44, "雖用心計，事難遂願，貪功好進，必招失敗。", "凶", -1.0f),
			new Rule(45, "楊柳遇春，綠葉發枝，沖?難關，一舉成名。", "吉", 1.0f),
			new Rule(46, "坎坷不平，?難重重，若無耐心，難望有成。", "凶", -1.0f),
			new Rule(47, "有貴人助，可成大業，雖遇不幸，浮沉不大。", "吉", 1.0f),
			new Rule(48, "美花豐實，鶴立雞群，名利俱全，繁榮富貴。", "吉", 1.0f),
			new Rule(49, "遇吉則吉，遇凶則凶，惟靠謹慎，逢凶化吉。", "凶", -1.0f),
			new Rule(50, "吉凶互見，一成一敗，凶中有吉，吉中有凶。", "吉帶凶", -0.5f),
			new Rule(51, "一盛一衰，浮沉不常，自重自處，可保平安。", "吉帶凶", -0.5f),
			new Rule(52, "草木逢春，雨過天晴，渡過難關，即獲成功。", "吉", 1.0f),
			new Rule(53, "盛衰參半，外祥內苦，先吉後凶，先凶後吉。", "吉帶凶", -0.5f),
			new Rule(54, "雖傾全力，難望成功，此數大凶，最好改名。", "凶", -1.0f),
			new Rule(55, "外觀隆昌，內隱禍患，克服難關，?出泰運。", "吉帶凶", -0.5f),
			new Rule(56, "事與願違，終難成功，欲速不達，有始無終。", "凶", -1.0f),
			new Rule(57, "雖有困難，時來運轉，曠野枯草，春來花?。", "凶帶吉", -0.75f),
			new Rule(58, "半凶半吉，浮沉多端，始凶終吉，能保成功。", "凶帶吉", -0.75f),
			new Rule(59, "遇事猶疑，難望成事，大刀闊斧，始可有成。", "凶", -1.0f),
			new Rule(60, "黑暗無光，心迷意亂，出爾反爾，難定方針。", "凶", -1.0f),
			new Rule(61, "雲遮半月，內隱風波，應自謹慎，始保平安。", "吉帶凶", -0.5f),
			new Rule(62, "煩悶懊惱，事業難展，自防災禍，始免困境。", "凶", -1.0f),
			new Rule(63, "萬物化育，繁榮之象，專心一意，必能成功。", "吉", 1.0f),
			new Rule(64, "見異思遷，十九不成，徒勞無功，不如更名。", "凶", -1.0f),
			new Rule(65, "吉運自來，能亨盛名，把握機會，必獲成功。", "吉", 1.0f),
			new Rule(66, "黑夜漫長，進退維谷，內外不和，信用缺乏。", "凶", -1.0f),
			new Rule(67, "獨營事業，事事如意，功成名就，富貴自來。", "吉", 1.0f),
			new Rule(68, "思慮週祥，計劃力行，不失先機，可望成功。", "吉", 1.0f),
			new Rule(69, "動搖不安，常陷逆境，不得時運，難得利潤。", "凶", -1.0f),
			new Rule(70, "慘淡經營，難免貧困，此數不吉，最好改名。", "凶", -1.0f),
			new Rule(71, "吉凶參半，惟賴勇氣，貫徹力行，始可成功。", "吉帶凶", -0.5f),
			new Rule(72, "利害混集，凶多吉少，得而復失，難以安順。", "凶", -1.0f),
			new Rule(73, "安樂自來，自然吉祥，力行不懈，必能成功。", "吉", 1.0f),
			new Rule(74, "利不及費，坐食山空，如無智謀，難望成功。", "凶", -1.0f),
			new Rule(75, "吉中帶凶，欲速不達，進不好守，可保安祥。", "吉帶凶", -0.5f),
			new Rule(76, "此數大凶，?產之象，宜速改名，以避厄運。", "凶", -1.0f),
			new Rule(77, "先苦後甘，先甘後苦，如能守成，不致失敗。", "吉帶凶", -0.5f),
			new Rule(78, "有得有失，華而不實，須防劫財，始保安順。", "吉帶凶", -0.5f),
			new Rule(79, "如走夜路，前途無光，希望不大，勞而無功。", "凶", -1.0f),
			new Rule(80, "得而復失，枉費心機，守成無貧，可保安穩。", "吉帶凶", -0.5f),
			new Rule(81, "最極之數，還本歸元，能得繁榮，發達成功。", "吉", 1.0f), };

	static private class RuleCategory {
		List<Integer> index_set;
		String commentary;
		@SuppressWarnings("unused")
		boolean goodorbad;
		float score;

		public RuleCategory(List<Integer> idx_set, String comm, boolean gob, float sc) {
			index_set = idx_set;
			commentary = comm;
			goodorbad = gob;
			score = sc;

		}
	}

	/*
	 * "double brace initialization"
	 */
	@SuppressWarnings("serial")
	static private List<RuleCategory> categories = new ArrayList<RuleCategory>() {
		{

			add(new RuleCategory(
					Arrays.asList(new Integer[] { 1, 3, 5, 7, 8, 11, 13, 15, 16, 18, 21, 23, 24, 25, 31, 32, 33, 35, 37,
							39, 41, 45, 47, 48, 52, 57, 61, 63, 65, 67, 68, 81 }),
					"一,吉祥運暗示數（代表健全,幸福,名譽等）",
					true, 0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 6, 17, 26, 27, 29, 30, 38, 49, 51, 55, 58, 71, 73, 75 }),
					"二,次吉祥運暗示數（代表多少有些障礙，但能獲得吉運）",
					true, 0.25f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 2, 4, 9, 10, 12, 14, 19, 20, 22, 28, 34, 36, 40, 42, 43, 44, 46, 50,
							53, 54, 56, 59, 60, 62, 64, 66, 69,
							70, 72, 74, 76, 77, 78, 79, 80 }),
					"三,凶數運暗示數（代表逆境,沉浮,薄弱,病難,困難,多災等）",
					false, -0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 3, 13, 16, 21, 23, 29, 31, 37, 39, 41, 45, 47 }),
					"四,首領運暗示數（智慧仁勇全備,立上位,能領導眾人）",
					true, 0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 15, 16, 24, 29, 32, 33, 41, 52 }),
					"五,財富運暗示數（多錢財,富貴,白手可獲巨財）",
					true, 0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 13, 14, 18, 26, 29, 33, 35, 38, 48 }),
					"六,藝能運暗示數（富有藝術天才，對審美,藝術,演藝,體育有通達之能）",
					true, 0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 5, 6, 11, 13, 15, 16, 24, 32, 35 }),
					"七,女德運暗示數（具有婦德，品性溫良，助夫愛子）",
					true, 0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 21, 23, 26, 28, 29, 33, 39 }),
					"八,女性孤寡運暗示數（難覓夫君，家庭不和，夫妻兩虎相鬥，離婚，嚴重者夫妻一方早亡）",
					false, -0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 4, 10, 12, 14, 22, 28, 34 }),
					"九,孤獨運暗示數（妻凌夫或夫克妻）",
					false, -0.5f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 5, 6, 15, 16, 32, 39, 41 }),
					"十,雙妻運暗示數",
					false, -0.25f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 7, 17, 18, 25, 27, 28, 37, 47 }),
					"十一,剛情運暗示數（性剛固執,意氣用事）",
					false, -0.25f));
			add(new RuleCategory(
					Arrays.asList(new Integer[] { 5, 6, 11, 15, 16, 24, 31, 32, 35 }),
					"十二,溫和運暗示數（性情平和,能得上下信望）",
					true, 0.5f));

		}
	};

	static public CheckResult checkRule(int num) {

		CheckResult result = new CheckResult();

		result.puregood = true;

		/*
		 * 1st. check mod
		 */
		int mod = num - (num / 80) * 80;
		int index;

		if (mod == 0)
			mod = 80;
		index = mod - 1;

		if (record[index].score < 0)
			result.puregood = false;
		result.score = record[index].score;
		result.commentaries
				.add(String.format("%d:%s:%s<%.2f>", record[index].index, record[index].goodorbad,
						record[index].commentary, result.score));

		/*
		 * 2nd. Categories
		 */

		for (RuleCategory cat : categories) {
			if (cat.index_set.contains(mod)) {
				result.score += cat.score;
				result.commentaries.add(String.format("%s <%.2f>", cat.commentary, cat.score));
				if (cat.score < 0)
					result.puregood = false;
			}
		}

		return result;

	}

}
