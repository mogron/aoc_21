import os

fn main() {
	x := os.read_lines('./input.txt') or {panic('file not readable')}
	fish_string := x[0]
	fishes := fish_string.split(',').map(fn (w string) int {
		return w.int()
	})
	mut days := []i64{len: 9}
	for fish in fishes {
		days[fish] += 1
	}
	steps := 256
	for i := 0; i < steps; i++ {
		d0 := days[0]
		for j := 1; j < 9; j++ {
			days[j-1] = days[j]
		}
		days[8] = d0
		days[6] += d0
	}
	mut sum := i64(0)
	for day in days {
		sum += day
	}
	println(sum)
}
