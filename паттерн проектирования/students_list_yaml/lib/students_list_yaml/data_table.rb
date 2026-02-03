class DataTable
    def initialize(rows)
        @rows = rows.map { |x| x.freeze }
    end

    def get(row, col)
        @rows[row][col]
    end

    def rows
        @rows.length
    end

    def columns
        return 0 if @rows.empty?
        @rows[0].length
    end

    def to_s
        @rows.to_s
    end
end