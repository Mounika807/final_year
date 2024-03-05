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
        Schema::create('user_destinations', function (Blueprint $table) {
            $table->id("destination_id");
            $table->bigInteger("plan_id");
            $table->bigInteger("user_id");
            $table->string("destination_name");
            $table->dateTime("destination_datetime")->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('user_destinations');
    }
};
