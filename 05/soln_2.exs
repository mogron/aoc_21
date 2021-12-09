defmodule Soln do
  def sgn(x) when x > 0, do: 1
  def sgn(x) when x == 0, do: 0
  def sgn(x) when x < 0, do: -1

  def parse_coords(s) do
    String.split(s, ",")
    |> Enum.map(&String.trim/1)
    |> Enum.map(
      &(Integer.parse(&1)
        |> elem(0))
    )
  end

  def handle_line(s) do
    # return a map where the keys represent the points covered by the given line
    [start, end_] = String.split(s, "->")
    [x1, y1] = parse_coords(start)
    [x2, y2] = parse_coords(end_)
    xd = x2 - x1
    yd = y2 - y1
    x_step = sgn(xd)
    y_step = sgn(yd)
    steps = max(x_step * xd, y_step * yd)

    Enum.reduce(0..steps, %{}, fn step, acc ->
      Map.put(acc, {x1 + x_step * step, y1 + y_step * step}, 1)
    end)
  end
end

# pointless concurrent processing
File.stream!("input.txt")
|> Task.async_stream(&Soln.handle_line/1)
|> Enum.map(&elem(&1, 1))
|> Enum.reduce(fn x, y -> Map.merge(x, y, fn _, v1, v2 -> v1 + v2 end) end)
|> Enum.count(fn {_, cover_count} -> cover_count > 1 end)
|> IO.puts()
