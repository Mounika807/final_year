<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('plan_models', function (Blueprint $table) {
            $table->id("plan_id");
            $table->bigInteger("user_id");
            $table->string("plan_title");
            $table->string("budget")->nullable();
            $table->string("special_occasion")->nullable();
            $table->integer("no_of_people")->nullable();
            $table->boolean("first_time_visiting")->nullable();
            $table->string("type_of_trip")->nullable();
            $table->string("sort_preference")->nullable();
            $table->string("food_preference")->nullable();
            $table->string("food_cost")->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('plan_models');
    }
};
