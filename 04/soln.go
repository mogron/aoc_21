package main

import (
	"io"
	"log"
	"os"
	"strconv"
	"strings"
)

type BoardElement struct {
	Value    int
	IsMarked bool
}

type Board struct {
	Grid       [][]*BoardElement
	IsComplete bool
}

func (b Board) Value() int {
	res := 0
	for _, row := range b.Grid {
		for _, elem := range row {
			if !elem.IsMarked {
				res += elem.Value
			}
		}
	}
	return res
}

func (b *Board) CheckRowComplete(rowIdx int) bool {
	row := b.Grid[rowIdx]
	for _, elem := range row {
		if !elem.IsMarked {
			return false
		}
	}
	b.IsComplete = true
	return true
}

func (b *Board) CheckColComplete(colIdx int) bool {
	for _, row := range b.Grid {
		if !row[colIdx].IsMarked {
			return false
		}
	}
	b.IsComplete = true
	return true
}

func (b *Board) Mark(value int) {
	for rowIdx, row := range b.Grid {
		for colIdx, elem := range row {
			if elem.Value == value {
				elem.IsMarked = true
				b.CheckColComplete(colIdx)
				b.CheckRowComplete(rowIdx)
			}
		}
	}
}

func stringsToInts(xs []string) []int {
	numbers := make([]int, 0)
	for _, s := range xs {
		number, _ := strconv.Atoi(s)
		numbers = append(numbers, number)
	}
	return numbers
}

func intsToBoardElements(xs []int) []*BoardElement {
	elements := make([]*BoardElement, 0)
	for _, num := range xs {
		element := BoardElement{Value: num, IsMarked: false}
		elements = append(elements, &element)
	}
	return elements
}

func main() {
	inputFile, err := os.Open("input.txt")
	if err != nil {
		log.Fatalln(err)
	}

	fileContents, err := io.ReadAll(inputFile)
	if err != nil {
		log.Fatalln(err)
	}

	inputLines := strings.Split(string(fileContents), "\n")
	numbersStrings := strings.Split(inputLines[0], ",")
	numbers := stringsToInts(numbersStrings)
	n_boards := (len(inputLines) - 1) / 6
	boards := make([]*Board, 0)
	for i := 0; i < n_boards; i++ {
		startIdx := 2 + i*6
		rows := make([][]*BoardElement, 0)
		for k := startIdx; k < startIdx+5; k++ {
			rowStrings := strings.Fields(inputLines[k])
			rowNums := stringsToInts(rowStrings)
			elements := intsToBoardElements(rowNums)
			rows = append(rows, elements)
		}
		board := Board{Grid: rows, IsComplete: false}
		boards = append(boards, &board)
	}

	for _, number := range numbers {
		for _, board := range boards {
			board.Mark(number)
			if board.IsComplete {
				print(board.Value() * number)
				return
			}
		}
	}

}
