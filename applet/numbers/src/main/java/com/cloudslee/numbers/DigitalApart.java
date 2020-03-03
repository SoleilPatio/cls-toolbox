package com.cloudslee.numbers;

import java.util.ArrayList;
import java.util.List;

public class DigitalApart {
	private int m_number;
	private List<Integer> m_digitals = new ArrayList<Integer>();

	public DigitalApart setNumber(int num) {
		m_number = num;
		_apart_the_number();
		return this;
	}

	public int getNumber() {
		return m_number;
	}

	/**
	 * 
	 * @param index
	 *            : 0 is the total number. 1-n is the nth digital
	 * @return
	 */
	public int d(int index) {
		if (index >= m_digitals.size())
			return 0;

		return m_digitals.get(index);
	}

	public int magnitude() {
		return (m_digitals.size()-1);
	}

	private void _apart_the_number() {
		int magnitude = 0;
		int temp = m_number;
		int digit;

		m_digitals.clear();
		m_digitals.add(0, m_number);

		while (temp > 0) {

			digit = temp - (temp / 10) * 10;
			m_digitals.add(magnitude + 1, digit);
			temp /= 10;
			magnitude++;
		}

	}

	@Override
	public String toString() {
		String result;

		result = String.format("%d(%d):", m_number, magnitude());

		for (int i = 1; i <= magnitude(); i++) {
			result += String.format(" %d ", d(i));
		}

		return result;
	}

}
