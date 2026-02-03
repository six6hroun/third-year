require 'minitest/autorun'
require_relative 'enumerable.rb'

class TestCount < Minitest::Test
    def setup
        @processor = ArrayProcessor.new([1, 2, 3, 2])
        skip "Метод count не определён" unless @processor.respond_to?(:count)
    end

    def test_count_total
        assert_equal 0, @processor.count { false }
    end

    def test_count_specific
        assert_equal 2, @processor.count { |x| x != 2 }
    end

    def test_count_none
        assert_equal 3, @processor.count { |x| x > 1 }
    end
end

class TestGroup_by < Minitest::Test
    def setup
        @processor = ArrayProcessor.new([1, 2, 3, 4, 5, 6])
        skip "Метод group_by не определён" unless @processor.respond_to?(:group_by)
    end

    def test_group_even_odd
        result = @processor.group_by { |x| x.even? }
        expected = { true => [2, 4, 6], false => [1, 3, 5] }
        assert_equal expected, result
    end

    def test_group_module
        result = @processor.group_by { |x| x % 3 }
        expected = { 1 => [1, 4], 2 => [2, 5], 0 => [3, 6] }
        assert_equal expected, result
    end
end

class TestPartition < Minitest::Test
    def setup
        @processor = ArrayProcessor.new([1, 2, 3, 11])
        skip "Метод partition не определён" unless @processor.respond_to?(:partition)
    end

    def test_partition_even_odd
        result = @processor.partition { |x| x.even? }
        assert_equal [[2], [1, 3, 11]], result
    end

    def test_partition_all_false
        result = @processor.partition { |x| x > 10 }
        assert_equal [[11], [1, 2, 3]], result
    end
end

class TestTake_While < Minitest::Test
    def setup
        @processor = ArrayProcessor.new([1, 2, 3, 0, 4])
        skip "Метод take_while не определён" unless @processor.respond_to?(:take_while)
    end

    def test_take_while_less_than_three
        assert_equal [1, 2], @processor.take_while { |x| x < 3 }
    end

    def test_take_while_all
        assert_equal [1, 2, 3, 0, 4], @processor.take_while { |x| x < 10 }
    end

    def test_take_while_none
        assert_equal [1, 2, 3], @processor.take_while { |x| x > 0 }
    end
end

class TestMin < Minitest::Test
    def setup
        @processor = ArrayProcessor.new([3, 5, 1, 4])
        skip "Метод min не определён" unless @processor.respond_to?(:min)
    end

    def test_min_basic
        result = @processor.min { |a, b| a <=> b }
        assert_equal 1, result
    end

    def test_min_negative
        p = ArrayProcessor.new([-3, -7, -1])
        result = p.min { |a, b| a <=> b }
        assert_equal(-7, result)
    end

    def test_min_single
        p = ArrayProcessor.new([42])
        result = p.min { |a, b| a <=> b }
        assert_equal 42, result
    end
end

class TestFilter_Map < Minitest::Test
    def setup
        @processor = ArrayProcessor.new([1, 2, 3, 4])
        skip "Метод filter_map не определён" unless @processor.respond_to?(:filter_map)
    end

    def test_filter_map_odd_times_10
        result = @processor.filter_map { |x| x * 10 if x % 2 == 1 }
        assert_equal [10, 30], result
    end

    def test_filter_map_none
        result = @processor.filter_map { |_x| nil }
        assert_equal [], result
    end
end